import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from rag.retriever import retrieve_documents


def test_rag_retriever_returns_documents():
    query = """
    CV:
    I know Python, SQL, machine learning, and data analysis.

    Target Role:
    Data Analyst Intern
    """

    results = retrieve_documents(
        query=query,
        top_k=3,
        category="job_descriptions"
    )

    assert len(results) > 0
    assert results[0]["category"] == "job_descriptions"
    assert "content" in results[0]
    assert "score" in results[0]


def test_rag_retriever_finds_data_analyst_role():
    query = "Python SQL Excel data visualization dashboard reporting"

    results = retrieve_documents(
        query=query,
        top_k=3,
        category="job_descriptions"
    )

    combined_content = " ".join([doc["content"] for doc in results])

    assert "Data Analyst Intern" in combined_content