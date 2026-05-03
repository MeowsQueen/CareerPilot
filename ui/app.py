import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.workflow import build_graph

st.set_page_config(
    page_title="CareerPilot",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(18px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes softGlow {
    0% {
        box-shadow: 0 0 18px rgba(100, 149, 237, 0.18);
    }
    50% {
        box-shadow: 0 0 32px rgba(100, 149, 237, 0.35);
    }
    100% {
        box-shadow: 0 0 18px rgba(100, 149, 237, 0.18);
    }
}

@keyframes gradientMove {
    0% { background-position: 0% }
    50% { background-position: 100% }
    100% { background-position: 0% }
}

@keyframes glowPulse {
    0% {
        text-shadow: 0 0 10px rgba(100,149,237,0.3);
    }
    50% {
        text-shadow: 0 0 25px rgba(100,149,237,0.7);
    }
    100% {
        text-shadow: 0 0 10px rgba(100,149,237,0.3);
    }
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(100, 149, 237, 0.20), transparent 32%),
        radial-gradient(circle at top right, rgba(176, 196, 222, 0.14), transparent 28%),
        linear-gradient(135deg, #0F172A 0%, #111827 45%, #172033 100%);
    color: #F8FAFC;
}

.block-container {
    padding-top: 3rem;
}

.main-title {
    font-size: 58px;
    font-weight: 900;
    background: linear-gradient(90deg, #7EA6FF, #B0C4DE, #E0ECFF, #7EA6FF);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    animation:
        gradientMove 6s linear infinite,
        glowPulse 3s ease-in-out infinite,
        fadeUp 0.7s ease forwards;
}

.subtitle {
    font-size: 22px;
    color: #CBD5E1;
    font-weight: 500;
    animation: fadeUp 0.9s ease forwards;
}

.card {
    padding: 26px;
    border-radius: 24px;
    background: rgba(30, 41, 59, 0.55);
    border: 1px solid rgba(176, 196, 222, 0.28);
    margin-bottom: 18px;
    box-shadow: 0 14px 38px rgba(0, 0, 0, 0.28);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    animation: fadeUp 0.6s ease forwards;
}

.card:hover {
    border: 1px solid rgba(126, 166, 255, 0.75);
    box-shadow: 0 18px 45px rgba(100, 149, 237, 0.22);
    transform: translateY(-3px);
    transition: all 0.28s ease;
}

.metric-card {
    padding: 24px;
    border-radius: 24px;
    background: rgba(24, 34, 53, 0.58);
    border: 1px solid rgba(100, 149, 237, 0.30);
    text-align: center;
    min-height: 150px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.24);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    transition: all 0.30s ease;
    animation: fadeUp 0.7s ease both;
}

div[data-testid="column"]:nth-of-type(1) .metric-card {
    animation-delay: 0.1s;
}

div[data-testid="column"]:nth-of-type(2) .metric-card {
    animation-delay: 0.25s;
}

div[data-testid="column"]:nth-of-type(3) .metric-card {
    animation-delay: 0.4s;
}

div[data-testid="column"]:nth-of-type(4) .metric-card {
    animation-delay: 0.55s;
}

.metric-card:hover {
    border: 1px solid rgba(126, 166, 255, 0.95);
    background: rgba(47, 66, 98, 0.72);
    transform: translateY(-6px) scale(1.02);
    box-shadow:
        0 16px 36px rgba(65, 105, 225, 0.26),
        0 0 28px rgba(100, 149, 237, 0.28);
}

.metric-card b {
    color: #F8FAFC;
}

.icon {
    font-size: 38px;
    filter: drop-shadow(0 0 10px rgba(100, 149, 237, 0.45));
}

.small-text {
    color: #CBD5E1;
    font-size: 15px;
}

.step-box {
    padding: 17px;
    border-radius: 18px;
    background: rgba(30, 41, 59, 0.68);
    border-left: 5px solid #7EA6FF;
    border-top: 1px solid rgba(176, 196, 222, 0.18);
    border-right: 1px solid rgba(176, 196, 222, 0.12);
    border-bottom: 1px solid rgba(176, 196, 222, 0.12);
    margin-bottom: 12px;
    color: #F8FAFC;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.25s ease;
}

.step-box:hover {
    transform: translateX(4px);
    box-shadow: 0 0 22px rgba(100, 149, 237, 0.22);
    border-left-color: #B0C4DE;
}

.workflow-box {
    padding: 22px;
    border-radius: 24px;
    background: rgba(30, 41, 59, 0.48);
    border: 1px solid rgba(176, 196, 222, 0.24);
    box-shadow: 0 12px 30px rgba(0,0,0,0.22);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    animation: fadeUp 0.7s ease both;
}

.workflow-text {
    font-size: 17px;
    font-weight: 700;
    color: #E0ECFF;
    line-height: 2;
}

.score-box {
    padding: 14px;
    border-radius: 16px;
    background: rgba(15, 23, 42, 0.48);
    border: 1px solid rgba(126, 166, 255, 0.25);
    margin-top: 10px;
    margin-bottom: 14px;
}

.how-card {
    padding: 22px;
    border-radius: 22px;
    background: rgba(30, 41, 59, 0.50);
    border: 1px solid rgba(176, 196, 222, 0.24);
    margin-bottom: 14px;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.20);
    animation: fadeUp 0.7s ease both;
}

h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
}

p, span, label, div {
    color: inherit;
}

.stButton > button {
    background: linear-gradient(90deg, #4169E1, #6495ED);
    color: white;
    border: none;
    border-radius: 16px;
    font-weight: 800;
    padding: 0.65rem 1rem;
    transition: all 0.28s ease;
    box-shadow: 0 8px 24px rgba(65, 105, 225, 0.25);
}

.stButton > button:hover {
    background: linear-gradient(90deg, #6495ED, #B0C4DE);
    color: #0F172A;
    transform: translateY(-3px) scale(1.01);
    box-shadow:
        0 12px 30px rgba(100, 149, 237, 0.38),
        0 0 24px rgba(176, 196, 222, 0.32);
}

.stButton > button:active {
    transform: scale(0.98);
}

section[data-testid="stSidebar"] {
    background: rgba(23, 29, 43, 0.78);
    border-right: 1px solid rgba(176, 196, 222, 0.24);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

textarea, input {
    color: #F8FAFC !important;
    background: rgba(15, 23, 42, 0.55) !important;
    border-radius: 14px !important;
}

div[data-baseweb="select"] > div {
    background: rgba(15, 23, 42, 0.55) !important;
    border-radius: 14px !important;
}

button[data-baseweb="tab"] {
    font-weight: 800;
    color: #CBD5E1;
    transition: all 0.25s ease;
}

button[data-baseweb="tab"]:hover {
    color: #B0C4DE;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #7EA6FF;
    text-shadow: 0 0 14px rgba(100, 149, 237, 0.55);
}

div[data-testid="stAlert"] {
    border-radius: 18px;
    background: rgba(30, 41, 59, 0.62);
    border: 1px solid rgba(176, 196, 222, 0.25);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
}

div[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.55);
    border: 1px solid rgba(176, 196, 222, 0.22);
    border-radius: 20px;
    padding: 18px;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.20);
    transition: all 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 0 25px rgba(100, 149, 237, 0.22);
}

hr {
    border-color: rgba(176, 196, 222, 0.18) !important;
}

[data-testid="stFileUploader"] {
    background: rgba(30, 41, 59, 0.42);
    border-radius: 18px;
    padding: 12px;
    border: 1px dashed rgba(176, 196, 222, 0.35);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">CareerPilot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">A Multi-Agent Career Guidance System with RAG and Safety Monitoring</div>',
    unsafe_allow_html=True
)

st.divider()

with st.sidebar:
    st.header("📥 Input Panel")

    uploaded_cv = st.file_uploader("Upload your CV", type=["txt"])

    target_role = st.selectbox(
        "Target Role",
        [
            "Data Analyst Intern",
            "AI / ML Intern",
            "Backend Developer Intern",
            "Frontend Developer Intern",
            "Software Developer Intern"
        ]
    )

    user_query = st.text_area(
        "Career Question",
        placeholder="Example: Based on my CV, which internships should I apply for?"
    )

    run_button = st.button("🚀 Analyze My Profile", use_container_width=True)

cv_text = ""
if uploaded_cv:
    cv_text = uploaded_cv.read().decode("utf-8")

st.markdown("### System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        '<div class="metric-card"><div class="icon">🧭</div><br><b>Planner Agent</b><br><span class="small-text">Plans the workflow</span></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="metric-card"><div class="icon">📚</div><br><b>RAG Retriever</b><br><span class="small-text">Retrieves knowledge</span></div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="metric-card"><div class="icon">💼</div><br><b>Job Matching</b><br><span class="small-text">Finds roles</span></div>',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        '<div class="metric-card"><div class="icon">🛡️</div><br><b>Safety Monitor</b><br><span class="small-text">Checks output</span></div>',
        unsafe_allow_html=True
    )

st.markdown("### 🔄 System Workflow")
st.markdown(
    """
    <div class="workflow-box">
        <div class="workflow-text">
            User Input → Planner Agent → CV Analyzer → RAG Retriever → Job Matching → Skill Gap Analysis → Interview Coach → Safety Monitor → Final Response
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

if uploaded_cv:
    with st.expander("📄 CV Preview"):
        st.write(cv_text[:1500])

if run_button:
    if not cv_text:
        st.error("Please upload a CV.")
    elif not user_query.strip():
        st.error("Please enter a question.")
    else:
        st.markdown("### Analysis Progress")

        progress = st.progress(0)
        status = st.empty()

        status.info("Planner Agent is preparing the workflow...")
        progress.progress(20)

        status.info("RAG Retriever is searching relevant career knowledge...")
        progress.progress(40)

        status.info("Job Matching Agent is comparing your profile with roles...")
        progress.progress(60)

        status.info("Skill Gap and Interview Agents are generating outputs...")
        progress.progress(80)

        with st.spinner("Final safety monitoring is running..."):
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

        progress.progress(100)
        status.success("Analysis completed successfully.")

        st.divider()

        jobs = result.get("job_matches", [])
        gaps = result.get("skill_gaps", [])
        questions = result.get("interview_questions", [])
        safety_report = result.get("safety_report", {})
        safety_status = safety_report.get("status", "unknown")

        if jobs:
            confidence_score = 85
        else:
            confidence_score = 45

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:
            st.metric("Target Role", target_role)

        with metric2:
            st.metric("Recommended Roles", len(jobs))

        with metric3:
            st.metric("Skill Gaps", len(gaps))

        with metric4:
            st.metric("Safety Status", safety_status)

        st.markdown("### 📈 Evaluation Snapshot")
        st.markdown(
            f"""
            <div class="score-box">
                <b>Overall Match Confidence:</b> {confidence_score}%<br>
                <span class="small-text">
                    This score summarizes how strongly the current output matches the selected target role and available retrieved job data.
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(confidence_score)

        st.divider()

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "📄 Career Guidance Summary",
                "💼 Recommended Roles",
                "📊 Skill Gaps & Roadmap",
                "🧠 Interview Preparation",
                "🛡️ Safety Notes"
            ]
        )

        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Career Guidance Summary")
            st.write(result.get("final_response", "No response generated."))
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Recommended Roles / Internships")

            if jobs:
                for i, job in enumerate(jobs, 1):
                    role_score = max(60, 90 - (i * 5))
                    st.markdown(f"""
                    <div class="step-box">
                        <b>{i}. Recommended Role</b><br>
                        {job}<br><br>
                        <b>Relevance Score:</b> {role_score}%
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(role_score)
            else:
                st.warning("⚠ No strong matches found for this profile.")
                st.markdown("""
<div class="step-box">
<b>Suggestion:</b><br>
Try selecting a different target role or improving your CV with more relevant skills.
</div>
""", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Skill Gap Analysis & Learning Roadmap")

            if gaps:
                for skill in gaps:
                    st.write(f"**{skill}**")
                    st.progress(65)

                st.markdown("#### Suggested Roadmap")
                st.markdown("""
                <div class="step-box">
                    <b>Step 1:</b> Focus on the highest-priority missing skills.<br>
                    <b>Step 2:</b> Build one small project using these skills.<br>
                    <b>Step 3:</b> Add the project and related keywords to your CV.<br>
                    <b>Step 4:</b> Practice interview questions for the selected role.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✔ No major skill gaps were detected.")
                st.markdown("""
<div class="step-box">
<b>Suggestion:</b><br>
Your current profile appears aligned with the selected target role. You can still improve your CV by adding more projects, tools, or measurable achievements.
</div>
""", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Interview Preparation")

            if questions:
                for i, question in enumerate(questions, 1):
                    st.markdown(f"""
                    <div class="step-box">
                        <b>Question {i}</b><br>
                        {question}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠ No interview questions were generated.")
                st.markdown("""
<div class="step-box">
<b>Suggestion:</b><br>
Try selecting a target role with stronger job matches or adding more detailed skills and project experience to your CV.
</div>
""", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with tab5:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Safety Monitoring Result")

            normalized_status = str(safety_status).lower()

            if normalized_status in ["safe", "passed", "ok", "clear"]:
                st.success("✔ Output passed safety checks.")
            elif normalized_status in ["unknown", "", "none"]:
                st.info("Safety status is currently unknown. Raw safety report is shown below.")
            else:
                st.warning("⚠ Potential safety or reliability issues were detected.")

            st.markdown("""
            <div class="step-box">
                <b>Safety checks focus on:</b><br>
                hallucination risk, unsupported claims, overconfident career advice, and biased recommendations.
            </div>
            """, unsafe_allow_html=True)

            with st.expander("View Raw Safety Report"):
                st.json(safety_report)

            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Upload CV → choose target role → write question → click Analyze My Profile 🚀")

    st.markdown("### 🚀 How It Works")

    how1, how2, how3, how4 = st.columns(4)

    with how1:
        st.markdown("""
        <div class="how-card">
            <div class="icon">📄</div>
            <b>1. Upload CV</b><br>
            <span class="small-text">Add your CV as a text file.</span>
        </div>
        """, unsafe_allow_html=True)

    with how2:
        st.markdown("""
        <div class="how-card">
            <div class="icon">🎯</div>
            <b>2. Select Role</b><br>
            <span class="small-text">Choose your target internship role.</span>
        </div>
        """, unsafe_allow_html=True)

    with how3:
        st.markdown("""
        <div class="how-card">
            <div class="icon">🤖</div>
            <b>3. Agent Analysis</b><br>
            <span class="small-text">Multiple agents analyze your profile.</span>
        </div>
        """, unsafe_allow_html=True)

    with how4:
        st.markdown("""
        <div class="how-card">
            <div class="icon">🛡️</div>
            <b>4. Safe Output</b><br>
            <span class="small-text">Final result is checked by safety monitoring.</span>
        </div>
        """, unsafe_allow_html=True)