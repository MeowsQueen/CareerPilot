from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, START, END

from rag.retriever import retrieve_documents


class CareerPilotState(TypedDict):
    user_query: str
    cv_text: str
    target_role: str
    plan: Dict[str, Any]
    cv_profile: Dict[str, Any]
    retrieved_jobs: List[Dict[str, Any]]
    job_matches: List[Dict[str, Any]]
    skill_gaps: List[str]
    interview_questions: List[str]
    final_response: str
    safety_report: Dict[str, Any]


def planner_node(state: CareerPilotState) -> CareerPilotState:
    state["plan"] = {
        "user_intent": "cv_based_career_guidance",
        "execution_order": [
            "cv_analyzer",
            "rag_retriever",
            "job_matcher",
            "skill_gap",
            "interview_coach",
            "safety_monitor"
        ],
        "reason": "The user provided a CV and target role for career guidance."
    }
    return state


def cv_analyzer_node(state: CareerPilotState) -> CareerPilotState:
    state["cv_profile"] = {
        "skills": ["Python", "SQL", "Machine Learning"],
        "education": "Computer Engineering student",
        "experience_level": "Internship"
    }
    return state


def rag_retriever_node(state: CareerPilotState) -> CareerPilotState:
    query = f"""
    CV:
    {state["cv_text"]}

    Target Role:
    {state["target_role"]}
    """

    retrieved = retrieve_documents(query, top_k=5)
    jobs = [doc for doc in retrieved if doc["category"] == "job_descriptions"]

    state["retrieved_jobs"] = jobs

    print("RETRIEVED DOCS:", state["retrieved_jobs"])

    return state


def extract_title(content: str) -> str:
    for line in content.splitlines():
        if line.lower().startswith("title:"):
            return line.replace("Title:", "").strip()
    return "Unknown Role"


def job_matcher_node(state: CareerPilotState) -> CareerPilotState:
    retrieved_jobs = state.get("retrieved_jobs", [])

    job_matches = []

    for job in retrieved_jobs:
        title = extract_title(job["content"])

        job_matches.append({
            "title": title,
            "match_reason": (
                f"This role was retrieved from the RAG knowledge base "
                f"based on the user's CV and target role: {state['target_role']}."
            ),
            "retrieval_score": job["score"],
            "source": job["id"]
        })

    state["job_matches"] = job_matches

    return state


def skill_gap_node(state: CareerPilotState) -> CareerPilotState:
    state["skill_gaps"] = ["Power BI", "Advanced Excel"]
    return state


def interview_coach_node(state: CareerPilotState) -> CareerPilotState:
    state["interview_questions"] = [
        "Can you explain a data analysis project you worked on?",
        "How would you clean a dataset with missing values?"
    ]
    return state


def safety_monitor_node(state: CareerPilotState) -> CareerPilotState:
    state["safety_report"] = {
        "status": "safe",
        "issues": []
    }

    state["final_response"] = f"""
CareerPilot Analysis

Target Role: {state["target_role"]}

Recommended Job:
{state["job_matches"][0]["title"]}

Skill Gaps:
{", ".join(state["skill_gaps"])}

Interview Questions:
1. {state["interview_questions"][0]}
2. {state["interview_questions"][1]}

Safety Status:
{state["safety_report"]["status"]}
"""
    return state


def build_graph():
    graph = StateGraph(CareerPilotState)

    graph.add_node("planner", planner_node)
    graph.add_node("cv_analyzer", cv_analyzer_node)
    graph.add_node("rag_retriever", rag_retriever_node)
    graph.add_node("job_matcher", job_matcher_node)
    graph.add_node("skill_gap", skill_gap_node)
    graph.add_node("interview_coach", interview_coach_node)
    graph.add_node("safety_monitor", safety_monitor_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "cv_analyzer")
    graph.add_edge("cv_analyzer", "rag_retriever")
    graph.add_edge("rag_retriever", "job_matcher")
    graph.add_edge("job_matcher", "skill_gap")
    graph.add_edge("skill_gap", "interview_coach")
    graph.add_edge("interview_coach", "safety_monitor")
    graph.add_edge("safety_monitor", END)

    return graph.compile()