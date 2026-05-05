from agents.state import CareerPilotState

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