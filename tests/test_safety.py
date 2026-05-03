import sys
from pathlib import Path

# Setup the root directory so the script can find the 'agents' and 'monitoring' packages
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from agents.safety import safety_monitor_node

def test_safety_agent_blocks_out_of_scope_query():
    """
    Test that the semantic/keyword audit catches non-career queries.
    """
    state = {
        "user_query": "Give me some cooking advice.",
        "cv_text": "Experienced software engineer with a focus on Python.",
        "target_role": "Senior Developer",
        "job_matches": [],
        "retrieved_jobs": []
    }
    
    result_state = safety_monitor_node(state)
    
    # Assertions to verify the gatekeeper blocked the request
    assert result_state["safety_report"]["status"] == "FAIL"
    assert "scope" in result_state["final_response"].lower() or "forbidden" in result_state["final_response"].lower()

def test_safety_agent_passes_valid_career_query():
    """
    Test that valid career queries pass through the safety node successfully.
    """
    state = {
        "user_query": "I want to apply for a Data Analyst role.",
        "cv_text": "I know Python, SQL, and Tableau.",
        "target_role": "Data Analyst",
        "job_matches": [{"title": "Data Analyst Intern"}],
        "retrieved_jobs": [{"content": "We are looking for a Data Analyst Intern with Python skills."}],
        "skill_gaps": ["Excel"],
        "interview_questions": ["Tell me about your SQL experience."]
    }
    
    result_state = safety_monitor_node(state)
    
    # Assertions to verify the passage of valid data
    assert result_state["safety_report"]["status"] == "PASS"
    assert "CareerPilot Analysis" in result_state["final_response"]
    assert "Data Analyst Intern" in result_state["final_response"]

def test_safety_agent_detects_hallucination():
    """
    Test that the agent catches job recommendations not present in the RAG data.
    """
    state = {
        "user_query": "Find me a job.",
        "cv_text": "Software engineer.",
        "target_role": "Developer",
        "job_matches": [{"title": "Astronaut"}], # Hallucinated title
        "retrieved_jobs": [{"content": "Web Developer position available."}] # Title doesn't match
    }
    
    result_state = safety_monitor_node(state)
    
    assert result_state["safety_report"]["status"] == "FAIL"
    assert "Hallucination" in result_state["safety_report"]["issues"][0]