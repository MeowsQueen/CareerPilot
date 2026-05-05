from pathlib import Path
import chromadb

from rag.embeddings import embed_text
from rag.chunking import chunk_text


ROOT_DIR = Path(__file__).resolve().parents[1]

BASE_DATA_DIR = ROOT_DIR / "rag" / "data"
DB_DIR = ROOT_DIR / "rag" / "vector_store"
COLLECTION_NAME = "career_knowledge"


def load_documents():
    documents = []

    if not BASE_DATA_DIR.exists():
        print(f"Data directory not found: {BASE_DATA_DIR}")
        return documents

    for category_path in BASE_DATA_DIR.iterdir():
        if not category_path.is_dir():
            continue

        category = category_path.name

        for file_path in category_path.glob("*.txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            doc_id = f"{category}_{file_path.stem}"

            documents.append({
                "id": doc_id,
                "text": text,
                "source": file_path.name,
                "category": category
            })

    return documents


def ingest_documents():
    client = chromadb.PersistentClient(path=str(DB_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    documents = load_documents()

    if not documents:
        print(f"No documents found in {BASE_DATA_DIR}")
        return

    total_chunks = 0

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for index, chunk in enumerate(chunks):
            chunk_id = f"{doc['id']}_chunk_{index}"
            embedding = embed_text(chunk)

            collection.upsert(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "source": doc["source"],
                    "category": doc["category"],
                    "parent_id": doc["id"],
                    "chunk_index": index
                }]
            )

            total_chunks += 1

    print(f"{len(documents)} documents loaded.")
    print(f"{total_chunks} chunks ingested into ChromaDB.")
    print(f"Database path: {DB_DIR}")
    print(f"Collection name: {COLLECTION_NAME}")


if __name__ == "__main__":
    ingest_documents()
