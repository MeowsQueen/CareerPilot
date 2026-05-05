from agents.state import CareerPilotState
from agents.job_matcher import extract_required_skills
 
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