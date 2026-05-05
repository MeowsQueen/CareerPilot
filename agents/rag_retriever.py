from agents.state import CareerPilotState
from rag.retriever import retrieve_documents

def rag_retriever_node(state: CareerPilotState) -> CareerPilotState:
    query = f"""
    Target Role:
    {state["target_role"]}

    Target Role:
    {state["target_role"]}

    CV:
    {state["cv_text"]}
    """

    jobs = retrieve_documents(
        query=query,
        top_k=3,
        category="job_descriptions"
    )

    state["retrieved_jobs"] = jobs

    return state