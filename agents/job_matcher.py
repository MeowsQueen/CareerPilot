from agents.state import CareerPilotState

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