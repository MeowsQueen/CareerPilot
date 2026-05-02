"""
RAG package for CareerPilot.

This package contains:
- document ingestion
- text chunking
- embedding utilities
- ChromaDB retrieval logic
"""

from rag.retriever import retrieve_documents

__all__ = ["retrieve_documents"]
