import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-3.1-flash-lite-preview"

TOP_K_RETRIEVAL = 3
COLLECTION_NAME = "career_knowledge"
VECTOR_STORE_PATH = "rag/vector_store"
