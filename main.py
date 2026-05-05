from agents.workflow import build_graph

app = build_graph()

initial_state = {
    "user_query": "I uploaded my CV and I want internship recommendations.",
    "cv_text": "I am a computer engineering student. I know Python, SQL, and machine learning.",
    "target_role": "Data Analyst Intern",
    "plan": {},
    "cv_profile": {},
    "retrieved_jobs": [],
    "job_matches": [],
    "skill_gaps": [],
    "interview_questions": [],
    "final_response": "",
    "safety_report": {}
}

result = app.invoke(initial_state)

print("PLAN:", result["plan"])
print(result["final_response"])