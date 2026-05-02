import os
import chromadb
from sentence_transformers import SentenceTransformer


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
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=DB_DIR)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    documents = load_documents()

    if not documents:
        print("No documents found in rag/data.")
        return

    for doc in documents:
        embedding = model.encode(doc["text"]).tolist()

        collection.upsert(
            ids=[doc["id"]],
            documents=[doc["text"]],
            embeddings=[embedding],
            metadatas=[{
                "source": doc["source"],
                "category": doc["category"]
            }]
        )

    print(f"{len(documents)} documents ingested into ChromaDB.")
    print(f"Database path: {DB_DIR}")
    print(f"Collection name: {COLLECTION_NAME}")


if __name__ == "__main__":
    ingest_documents()