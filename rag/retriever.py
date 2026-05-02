import chromadb
from sentence_transformers import SentenceTransformer


DB_DIR = "rag/vector_store"
COLLECTION_NAME = "career_knowledge"


model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def retrieve_documents(query: str, top_k: int = 3):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    docs = []

    for i in range(len(results["ids"][0])):
        docs.append({
            "id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "category": results["metadatas"][0][i]["category"],
            "score": results["distances"][0][i]
        })

    return docs