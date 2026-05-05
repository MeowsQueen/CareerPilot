from pathlib import Path
import chromadb

from rag.embeddings import embed_text


ROOT_DIR = Path(__file__).resolve().parents[1]

DB_DIR = ROOT_DIR / "rag" / "vector_store"
COLLECTION_NAME = "career_knowledge"


client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_collection(name=COLLECTION_NAME)



def retrieve_documents(query: str, top_k: int = 5, category: str | None = None):
    query_embedding = embed_text(query)

    where_filter = {"category": category} if category else None

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter
    )

    docs = []

    for i in range(len(results["ids"][0])):
        docs.append({
            "id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "category": results["metadatas"][0][i]["category"],
            "source": results["metadatas"][0][i]["source"],
            "parent_id": results["metadatas"][0][i].get("parent_id"),
            "chunk_index": results["metadatas"][0][i].get("chunk_index"),
            "score": results["distances"][0][i]
        })

    return docs
