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
│   │   └── rag_section.md
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

## RAG Setup and Usage

The RAG module uses ChromaDB as a local vector database and SentenceTransformers for embeddings.

### 1. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Ingest knowledge base documents

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

### 3. Run the system

```bash
python main.py
```

### 4. Run demo cases
```bash
python scripts/demo_cases.py
```

### 5. Run RAG tests

```bash
pytest tests/test_rag.py
```

Expected result:

```text
2 passed
```

### Note

`rag/vector_store/` is ignored by Git. Each developer should generate it locally by running:

```bash
python -m rag.ingest
```

ChromaDB distance scores are used for retrieval ranking. Lower distance means higher relevance.
