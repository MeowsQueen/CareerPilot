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

def extract_required_skills(content: str) -> list[str]:
    lines = content.splitlines()
    skills = []

    for i, line in enumerate(lines):
        if line.lower().startswith("required skills:"):
            if ":" in line and line.split(":", 1)[1].strip():
                skills_text = line.split(":", 1)[1]
            elif i + 1 < len(lines):
                skills_text = lines[i + 1]
            else:
                skills_text = ""

            skills = [skill.strip() for skill in skills_text.split(",") if skill.strip()]
            break

    return skills


def skill_gap_node(state: CareerPilotState) -> CareerPilotState:
    cv_skills = state.get("cv_profile", {}).get("skills", [])
    cv_skills_lower = [skill.lower() for skill in cv_skills]

    job_matches = state.get("job_matches", [])
    retrieved_jobs = state.get("retrieved_jobs", [])

    if not job_matches or not retrieved_jobs:
        state["skill_gaps"] = []
        return state

    best_match_source = job_matches[0]["source"]

    best_job = next(
        (job for job in retrieved_jobs if job["id"] == best_match_source),
        retrieved_jobs[0]
    )

    required_skills = extract_required_skills(best_job["content"])

    missing_skills = [
        skill for skill in required_skills
        if skill.lower() not in cv_skills_lower
    ]

    state["skill_gaps"] = missing_skills

    return state


def interview_coach_node(state: CareerPilotState) -> CareerPilotState:
    job_matches = state.get("job_matches", [])
    skill_gaps = state.get("skill_gaps", [])
    cv_skills = state.get("cv_profile", {}).get("skills", [])

    if not job_matches:
        state["interview_questions"] = []
        return state

    job_title = job_matches[0]["title"]

    questions = []

    # Role-based questions
    questions.append(f"What experience do you have related to the role of {job_title}?")
    questions.append(f"Can you explain a project where you used {', '.join(cv_skills[:2])}?")

    # Skill gap questions
    for skill in skill_gaps[:2]:
        questions.append(f"How would you approach learning or improving your skills in {skill}?")

    # Problem-solving
    questions.append("How would you approach solving a real-world problem in this role?")

    state["interview_questions"] = questions

    return state


def safety_monitor_node(state: CareerPilotState) -> CareerPilotState:
    state["safety_report"] = {
        "status": "safe",
        "issues": []
    }

    recommended_job = (
        state["job_matches"][0]["title"]
        if state.get("job_matches")
        else "No suitable job found."
    )

    skill_gaps_text = (
        ", ".join(state["skill_gaps"])
        if state.get("skill_gaps")
        else "No major skill gaps found."
    )

    questions_text = (
        "\n".join(
            [f"{i + 1}. {question}" for i, question in enumerate(state.get("interview_questions", []))]
        )
        if state.get("interview_questions")
        else "No interview questions generated."
    )

    state["final_response"] = f"""
CareerPilot Analysis

Target Role: {state["target_role"]}

Recommended Job:
{recommended_job}

Skill Gaps:
{skill_gaps_text}

Interview Questions:
{questions_text}

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