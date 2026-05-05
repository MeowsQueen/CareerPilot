from agents.state import CareerPilotState

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

def extract_title(content: str) -> str:
    for line in content.splitlines():
        if line.lower().startswith("title:"):
            return line.replace("Title:", "").strip()
    return "Unknown Role"