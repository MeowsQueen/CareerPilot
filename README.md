# CareerPilot: A Multi-Agent Career Mentor with RAG and Safety Monitoring

CareerPilot is a multi-agent career guidance system designed to help students analyze their CVs, identify suitable internship roles, detect skill gaps, generate interview questions, and receive safer AI-assisted career recommendations.

The system combines:

- Multi-agent orchestration
- Retrieval-Augmented Generation (RAG)
- ChromaDB vector search
- SentenceTransformers embeddings
- Safety monitoring
- Evaluation metrics
- Streamlit-based user interface

---

## Live Demo

🌐 Live Demo: https://careerpilot-a-multi-agent-career-mentor.streamlit.app/  
🎥 Demo Video: https://www.youtube.com/watch?v=TMf7xOI8Ups

---

## Features

- CV upload and analysis
- Target role selection
- RAG-based job retrieval
- Job matching
- Skill gap analysis
- Interview question generation
- Safety and hallucination monitoring
- Evaluation pipeline
- Streamlit UI

---

## System Workflow

```text
User Input
   ↓
Planner Agent
   ↓
CV Analyzer
   ↓
RAG Retriever
   ↓
Job Matcher
   ↓
Skill Gap Agent
   ↓
Interview Coach
   ↓
Safety Monitor
   ↓
Final Career Guidance Output
```

---

## Technology Stack

- Python
- LangGraph
- Google Gemini
- ChromaDB
- SentenceTransformers
- Streamlit
- PyPDF
- Pytest

---

## Repository Structure

```text
career-pilot/
│
├── agents/
│   ├── __init__.py
│   ├── planner.py
│   ├── cv_analyzer.py
│   ├── job_matcher.py
│   ├── skill_gap.py
│   ├── interview.py
│   ├── safety.py
│   └── workflow.py
│
├── rag/
│   ├── __init__.py
│   ├── ingest.py
│   ├── retriever.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── data/
│   │   ├── job_descriptions/
│   │   ├── cv_guidelines/
│   │   └── skill_roadmaps/
│   └── vector_store/
│
├── scripts/
│   └── demo_cases.py
│
├── monitoring/
│   ├── __init__.py
│   ├── safety_rules.py
│   ├── risk_checks.py
│   └── logs.py
│
├── evaluation/
│   ├── __init__.py
│   ├── metrics.py
│   ├── evaluator.py
│   ├── run_evaluation.py
│   ├── rubric.md
│   └── test_profiles/
│       ├── profile_01.json
│       ├── profile_02.json
│       ├── profile_03.json
│       ├── profile_04.json
│       └── profile_05.json
│
├── ui/
│   ├── __init__.py
│   └── app.py
│
├── utils/
│   ├── __init__.py
│   └── prompts.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── docs/
│   ├── report/
│   │   ├── rag_section.md
│   │   └── safety_section.md
│   ├── screenshots/
│   └── demo_notes.md
│
├── tests/
│   ├── test_agents.py
│   ├── test_rag.py
│   └── test_safety.py
│
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/MeowsQueen/CareerPilot.git
cd CareerPilot
```

### Create and Activate a Virtual Environment

```bash
python -m venv .venv
```

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## Environment Variables

Create a `.env` file in the project root and add your API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

## RAG Setup and Usage

The RAG module uses ChromaDB as a local vector database and SentenceTransformers for embeddings.

Before running the system, build the local vector database:

```bash
python -m rag.ingest
```

This reads documents from:

```text
rag/data/job_descriptions/
rag/data/cv_guidelines/
rag/data/skill_roadmaps/
```

and stores embeddings in:

```text
rag/vector_store/
```

### Important Note

`rag/vector_store/` is ignored by Git. Each developer should generate it locally by running:

```bash
python -m rag.ingest
```

ChromaDB distance scores are used for retrieval ranking. Lower distance means higher relevance.

---

## Running the System

### Run the Command-Line Version

```bash
python main.py
```

### Run the Streamlit UI

```bash
streamlit run ui/app.py
```

### Run Demo Cases

```bash
python scripts/demo_cases.py
```

### Run Evaluation

```bash
python -m evaluation.run_evaluation
```

---

## Running Tests

### Run RAG Tests

```bash
pytest tests/test_rag.py
```

Expected result:

```text
2 passed
```

### Run All Tests

```bash
pytest
```

---

## Evaluation

CareerPilot includes an evaluation pipeline based on both extrinsic and intrinsic metrics.

### Evaluation Metrics

- Top-3 Job Match Relevance
- Precision@3
- Skill Gap Correctness
- Interview Question Relevance
- Response Completeness
- Intrinsic Interview Question Quality Score

The evaluation module uses predefined test profiles located under:

```text
evaluation/test_profiles/
```

---

## Safety and Monitoring

CareerPilot includes a safety monitoring layer that checks:

- Forbidden or out-of-scope topics
- Hallucinated job recommendations
- Unsupported claims
- Overconfident career advice
- Unsafe or unreliable outputs

The safety module produces a `PASS` or `FAIL` status before the final response is shown to the user.

---

## Current Limitations

- Knowledge base size is limited
- Some domains are underrepresented
- CV skill extraction is simplified
- Retrieval uses dense vector search only
- No reranking model is currently applied
- Real-time job market APIs are not integrated yet

---

## Future Work

- DOCX CV parsing support
- Larger and more diverse knowledge base
- Hybrid retrieval and reranking
- Real-time job API integration
- More advanced CV parsing
- Personalized learning roadmaps
- Improved scalability and deployment

---

## Authors and Responsibilities

| Team Member | Responsibility |
|---|---|
| Süreyya YILDIRIM | Architecture & Planner |
| Beyza Nur YAZICI | RAG |
| Hacer Dilara KIVRAK | UI |
| Zehra Betül ŞİT | Safety & Monitoring |
| Ahsen DURSUN | Evaluation & Metrics |

---

## Project Summary

CareerPilot is a multi-agent career mentorship system that analyzes student CVs, retrieves relevant job knowledge from a vector database, recommends suitable opportunities, identifies skill gaps, generates interview questions, and monitors outputs for safety and reliability.

:contentReference[oaicite:0]{index=0}
