import sys
import os
import streamlit as st
from pypdf import PdfReader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.workflow import build_graph

st.set_page_config(
    page_title="CareerPilot",
    page_icon="🎓",
    layout="wide"
)

def get_job_title(job):
    if isinstance(job, dict):
        return job.get("title", "Recommended Role")
    return str(job)

def read_cv_file(uploaded_file):
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        try:
            return uploaded_file.read().decode("utf-8")
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return uploaded_file.read().decode("latin-1")

    elif file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    return ""

st.title("🎓 CareerPilot")
st.write("Multi-Agent Career Guidance System")

with st.sidebar:
    uploaded_cv = st.file_uploader("Upload your CV", type=["txt", "pdf"])

    target_role = st.selectbox(
        "Target Role",
        [
            "Data Analyst Intern",
            "Machine Learning Intern",
            "Backend Developer Intern",
            "Frontend Developer Intern",
            "Software Engineer Intern",
            "Data Scientist Intern",
            "Fullstack Developer Intern",
            "Mobile Developer Intern"
        ]
    )

    user_query = st.text_area("Career Question")
    run_button = st.button("🚀 Analyze")

cv_text = ""
if uploaded_cv:
    cv_text = read_cv_file(uploaded_cv)

if run_button:
    if not cv_text:
        st.error("Please upload a CV.")
    elif not user_query.strip():
        st.error("Please enter a question.")
    else:
        app = build_graph()

        initial_state = {
            "user_query": user_query,
            "cv_text": cv_text,
            "target_role": target_role,
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

        jobs = result.get("job_matches", [])
        gaps = result.get("skill_gaps", [])
        questions = result.get("interview_questions", [])

        st.subheader("📄 Summary")
        st.write(result.get("final_response", ""))

        st.subheader("💼 Recommended Roles")

        if jobs:
            for i, job in enumerate(jobs, 1):
                role_title = get_job_title(job)
                role_score = max(60, 90 - (i * 5))

                retrieval_score = job.get("retrieval_score", None) if isinstance(job, dict) else None
                match_reason = (
                    job.get("match_reason", "Retrieved from the RAG knowledge base.")
                    if isinstance(job, dict)
                    else "Retrieved from the RAG knowledge base."
                )

                score_text = (
                    f"RAG Distance Score: {retrieval_score:.4f}"
                    if retrieval_score is not None
                    else f"Relevance Score: {role_score}%"
                )

                st.write(f"### {role_title}")
                st.write(match_reason)
                st.write(score_text)
                st.progress(role_score)
        else:
            st.warning("No matches found.")

        st.subheader("📊 Skill Gaps")

        if gaps:
            for skill in gaps:
                st.write(f"- {skill}")
        else:
            st.success("No major skill gaps.")

        st.subheader("🧠 Interview Questions")

        if questions:
            for q in questions:
                st.write(f"- {q}")
        else:
            st.warning("No questions generated.")
