from agents.workflow import build_graph


app = build_graph()


demo_cases = [
    {
        "name": "Data Analyst Case",
        "user_query": "I want internship recommendations.",
        "cv_text": "I am a computer engineering student. I know Python, SQL, and machine learning.",
        "target_role": "Data Analyst Intern",
    },
    {
        "name": "Frontend Developer Case",
        "user_query": "I want frontend internship recommendations.",
        "cv_text": "I know HTML, CSS, JavaScript, React, Git, and responsive web design.",
        "target_role": "Frontend Developer Intern",
    },
    {
        "name": "Backend Developer Case",
        "user_query": "I want backend internship recommendations.",
        "cv_text": "I know Python, Java, SQL, REST APIs, Git, and backend development.",
        "target_role": "Backend Developer Intern",
    },
    {
        "name": "Machine Learning Case",
        "user_query": "I want machine learning internship recommendations.",
        "cv_text": "I know Python, NumPy, Pandas, Scikit-learn, machine learning, and data preprocessing.",
        "target_role": "Machine Learning Intern",
    },
]


def build_initial_state(case):
    return {
        "user_query": case["user_query"],
        "cv_text": case["cv_text"],
        "target_role": case["target_role"],
        "plan": {},
        "cv_profile": {},
        "retrieved_jobs": [],
        "job_matches": [],
        "skill_gaps": [],
        "interview_questions": [],
        "final_response": "",
        "safety_report": {},
    }


for case in demo_cases:
    print("=" * 80)
    print(case["name"])
    print("=" * 80)

    result = app.invoke(build_initial_state(case))

    print(result["final_response"])