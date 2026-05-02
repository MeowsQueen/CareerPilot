# CareerPilot-A-Multi-Agent-Career-Mentor-with-RAG-and-Safety-Monitoring

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
│   └── safety.py
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
│   ├── rubric.md
│   └── test_profiles/
│       ├── profile_01.json
│       ├── profile_02.json
│       ├── profile_03.json
│       └── profile_04.json
│
├── ui/
│   ├── __init__.py
│   └── app.py
│
├── utils/
│   ├── __init__.py
│   ├── cv_parser.py
│   ├── prompts.py
│   └── helpers.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── docs/
│   ├── report/
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
├── README.md
├── .env.example
└── .gitignore
```
