# Retrieval-Augmented Generation (RAG) Design

## Knowledge Base

The RAG module uses a local knowledge base stored under `rag/data/`. The knowledge base is divided into three categories:

- `job_descriptions/`: internship and junior role descriptions
- `cv_guidelines/`: CV writing and ATS-friendly resume guidelines
- `skill_roadmaps/`: role-based learning roadmaps

This structure allows the system to retrieve different types of career-related knowledge depending on the agent’s task.

## Embedding Model

The system uses the `all-MiniLM-L6-v2` model from SentenceTransformers to convert text documents and user queries into dense vector embeddings.

## Vector Database

ChromaDB is used as the local vector database. The embedded documents are stored in the `rag/vector_store/` directory. Each stored chunk includes metadata such as:

- source file
- document category
- parent document id
- chunk index

## Chunking Strategy

Before indexing, each document is processed with a simple word-based chunking function. Long documents are split into smaller chunks with overlap. This improves retrieval quality by allowing the system to match user queries with more focused parts of the knowledge base.

## Retrieval Flow

The retrieval process works as follows:

1. The user’s CV text and target role are combined into a query.
2. The query is converted into an embedding.
3. ChromaDB searches for the most similar document chunks.
4. The retriever applies category filtering, such as retrieving only `job_descriptions`.
5. Retrieved documents are passed to downstream agents, such as Job Matcher and Skill Gap Agent.

## Current Usage in Workflow

In the current system, the RAG retriever is used inside `rag_retriever_node`. It retrieves the top job descriptions related to the user’s CV and target role. These retrieved jobs are then used by:

- `job_matcher_node` for recommending relevant roles
- `skill_gap_node` for comparing CV skills with job requirements
- `interview_coach_node` for generating role-specific interview questions
