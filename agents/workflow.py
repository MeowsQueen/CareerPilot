import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, START, END


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
- If the user needs preparation for a role, include interview_coach.
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
    state["cv_profile"] = {
        "skills": ["Python", "SQL", "Machine Learning"],
        "education": "Computer Engineering student",
        "experience_level": "Internship"
    }
    return state


def rag_retriever_node(state: CareerPilotState) -> CareerPilotState:
    state["retrieved_jobs"] = [
        {
            "title": "Data Analyst Intern",
            "required_skills": ["Python", "SQL", "Excel", "Power BI"]
        },
        {
            "title": "Machine Learning Intern",
            "required_skills": ["Python", "Machine Learning", "Pandas", "Scikit-learn"]
        }
    ]
    return state


def job_matcher_node(state: CareerPilotState) -> CareerPilotState:
    state["job_matches"] = [
        {
            "title": "Data Analyst Intern",
            "match_reason": "The CV includes Python and SQL, which are core requirements."
        }
    ]
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

    job_matches = state.get("job_matches", [])
    skill_gaps = state.get("skill_gaps", [])
    interview_questions = state.get("interview_questions", [])

    recommended_job = job_matches[0]["title"] if job_matches else "No job recommendation generated."

    skill_gap_text = (
        ", ".join(skill_gaps)
        if skill_gaps
        else "No skill gap analysis generated."
    )

    if interview_questions:
        interview_text = "\n".join(
            f"{index + 1}. {question}"
            for index, question in enumerate(interview_questions)
        )
    else:
        interview_text = "No interview preparation requested."

    state["final_response"] = f"""
CareerPilot Analysis

Target Role: {state["target_role"]}

Recommended Job:
{recommended_job}

Skill Gaps:
{skill_gap_text}

Interview Questions:
{interview_text}

Safety Status:
{state["safety_report"]["status"]}
"""

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