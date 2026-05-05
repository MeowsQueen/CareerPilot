from typing import TypedDict, List, Dict, Any

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