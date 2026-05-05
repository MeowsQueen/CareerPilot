import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, START, END

from rag.retriever import retrieve_documents

from agents.safety import safety_monitor_node

# helper function 
def extract_job_title(content: str) -> str:
    lines = content.splitlines()

    for line in lines:
        lower_line = line.lower()

        if "title:" in lower_line:
            return line.split(":", 1)[1].strip()

        if "job title:" in lower_line:
            return line.split(":", 1)[1].strip()

        if "role:" in lower_line:
            return line.split(":", 1)[1].strip()

    return "Unknown Job"

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
    load_dotenv()

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )

    prompt = f"""
You are the Planner Agent of CareerPilot, a multi-agent AI career assistant.

Your task is to analyze the user's request and decide which agents should be executed.

Available agents:
- cv_analyzer
- rag_retriever
- job_matcher
- skill_gap
- interview_coach
- safety_monitor

User query:
{state["user_query"]}

CV text is provided: {bool(state["cv_text"])}
Target role: {state["target_role"]}

Return ONLY valid JSON in this format:

{{
  "user_intent": "...",
  "execution_order": ["cv_analyzer", "rag_retriever", "job_matcher", "skill_gap", "interview_coach", "safety_monitor"],
  "reason": "..."
}}

Rules:
- Always include safety_monitor as the last step.
- If CV text is provided, include cv_analyzer.
- If the user asks for job or internship recommendations, include rag_retriever and job_matcher.
- If a target role is provided, include skill_gap.
- If the user asks for job or internship recommendations, include interview_coach after skill_gap because the system should provide preparation material for the recommended role.
- Do not include explanations outside JSON.
"""

    response = llm.invoke(prompt)
    if isinstance(response.content, str):
        raw_text = response.content.strip()
    elif isinstance(response.content, list):
        raw_text = "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in response.content
        ).strip()
    else:
        raw_text = str(response.content).strip()

    try:
        json_start = raw_text.find("{")
        json_end = raw_text.rfind("}") + 1
        clean_json = raw_text[json_start:json_end]
        plan = json.loads(clean_json)

    except Exception:
        plan = {
            "user_intent": "planning_failed",
            "execution_order": [
                "cv_analyzer",
                "rag_retriever",
                "job_matcher",
                "skill_gap",
                "interview_coach",
                "safety_monitor"
            ],
            "reason": "Planner output could not be parsed, so the default workflow was used.",
            "raw_output": raw_text
        }

    state["plan"] = plan
    return state

def cv_analyzer_node(state: CareerPilotState) -> CareerPilotState:
    cv_text = state.get("cv_text", "")

    known_skills = [
        "python", "sql", "excel", "power bi", "tableau",
        "machine learning", "deep learning", "pandas", "numpy",
        "scikit-learn", "tensorflow", "pytorch",
        "html", "css", "javascript", "react", "node.js",
        "java", "c++", "git", "github", "fastapi", "django",
        "data visualization", "statistics", "nlp", "rag", "llm"
    ]

    extracted_skills = []

    lower_cv = cv_text.lower()

    for skill in known_skills:
        if skill in lower_cv:
            extracted_skills.append(skill.title())

    state["cv_profile"] = {
        "skills": extracted_skills,
        "education": "Extracted from CV text",
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
    cv_skills = [
        skill.lower()
        for skill in state.get("cv_profile", {}).get("skills", [])
    ]

    job_matches = []

    for job in retrieved_jobs:
        job_id = job.get("id")
        content = job.get("content", "")

        title = job.get("title", "Unknown Job")

        if title == "Unknown Job":
            title = extract_job_title(content)

        required_skills = job.get("required_skills", [])

        if not required_skills:
            required_skills = extract_required_skills(content)

        required_skills_lower = [
            skill.lower()
            for skill in required_skills
        ]

        matched_skills = [
            skill
            for skill in required_skills_lower
            if skill in cv_skills
        ]

        score = (
            len(matched_skills) / len(required_skills_lower)
            if required_skills_lower
            else 0
        )

        job_matches.append({
            "title": title,
            "source": job_id,
            "required_skills": required_skills,
            "matched_skills": matched_skills,
            "match_score": round(score, 2),
            "match_reason": (
                f"Matched skills: {', '.join(matched_skills)}"
                if matched_skills
                else "No direct skill match found."
            )
        })

    job_matches = sorted(
        job_matches,
        key=lambda x: x["match_score"],
        reverse=True
    )

    state["job_matches"] = job_matches[:3]

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

def agent_executor_node(state: CareerPilotState) -> CareerPilotState:
    agent_functions = {
        "cv_analyzer": cv_analyzer_node,
        "rag_retriever": rag_retriever_node,
        "job_matcher": job_matcher_node,
        "skill_gap": skill_gap_node,
        "interview_coach": interview_coach_node,
        "safety_monitor": safety_monitor_node,
    }

    execution_order = state["plan"].get("execution_order", [])

    for agent_name in execution_order:
        agent_function = agent_functions.get(agent_name)

        if agent_function is not None:
            state = agent_function(state)

    return state

def build_graph():
    graph = StateGraph(CareerPilotState)

    graph.add_node("planner", planner_node)
    graph.add_node("agent_executor", agent_executor_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "agent_executor")
    graph.add_edge("agent_executor", END)

    return graph.compile()