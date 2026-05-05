from monitoring.safety_rules import FORBIDDEN_TOPICS, BANNED_PHRASES, MIN_CONFIDENCE_SCORE

def check_hallucination(recommended_job, retrieved_jobs):
    """
    Verifies if the recommended job title is actually present in the 
    documents retrieved from the RAG database.
    """
    if not retrieved_jobs:
        return True  # If no jobs were found by RAG, any recommendation is a risk
    
    # We check if the title exists in the content of the retrieved documents
    found = any(recommended_job.lower() in job["content"].lower() for job in retrieved_jobs)
    return not found  # Returns True if it IS a hallucination

def check_forbidden_content(text, forbidden_list):
    """
    Scans the text for keywords that are out of scope (e.g., medical, baking).
    """
    # Now using the list passed from the agent
    found_topics = [topic for topic in forbidden_list if topic in text.lower()]
    return found_topics

def check_overconfidence(text):
    """
    Scans for aggressive or unrealistic promises like 'I guarantee'.
    """
    found_phrases = [phrase for phrase in BANNED_PHRASES if phrase in text.lower()]
    return found_phrases

def calculate_average_rag_score(retrieved_jobs):
    """
    Checks the mathematical 'distance' or 'score' from ChromaDB.
    Lower scores in ChromaDB usually mean higher similarity.
    """
    if not retrieved_jobs:
        return 0.0
    
    # ChromaDB scores are often distance-based (0 to 1+)
    scores = [job.get("score", 1.0) for job in retrieved_jobs]
    avg_score = sum(scores) / len(scores)
    return avg_score

def validate_rag_reliability(retrieved_jobs):
    """
    Uses the MIN_CONFIDENCE_SCORE to determine if the retrieved 
    data is strong enough to rely on.
    """
    avg = calculate_average_rag_score(retrieved_jobs)
    # If the average distance is too high, the match is weak
    if avg > (1 - MIN_CONFIDENCE_SCORE): 
        return False, f"Low retrieval relevance (Avg Score: {avg:.2f})"
    return True, "Reliable"