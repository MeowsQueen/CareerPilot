import os
import chromadb

from rag.embeddings import embed_text
from rag.chunking import chunk_text


BASE_DATA_DIR = "rag/data"
DB_DIR = "rag/vector_store"
COLLECTION_NAME = "career_knowledge"


def load_documents():
    documents = []

    for category in os.listdir(BASE_DATA_DIR):
        category_path = os.path.join(BASE_DATA_DIR, category)

        if not os.path.isdir(category_path):
            continue

        for filename in os.listdir(category_path):
            if not filename.endswith(".txt"):
                continue

            file_path = os.path.join(category_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            doc_id = f"{category}_{filename.replace('.txt', '')}"

            documents.append({
                "id": doc_id,
                "text": text,
                "source": filename,
                "category": category
            })

    return documents


def ingest_documents():
    client = chromadb.PersistentClient(path=DB_DIR)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    documents = load_documents()

    if not documents:
        print("No documents found in rag/data.")
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