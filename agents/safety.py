# agents/safety.py
import os
from monitoring import (
    FORBIDDEN_TOPICS, 
    SAFETY_MESSAGES, 
    check_hallucination, 
    check_forbidden_content, 
    log_safety_event
)

def safety_monitor_node(state):
    """
    Final node in the workflow: Audits for safety/hallucinations 
    and formats the final output for the user.
    """
    issues = []
    
    # --- 1. DATA GATHERING ---
    user_query = state.get("user_query", "")
    # Use cv_text if available, otherwise fallback to placeholder
    cv_input = state.get("cv_text", "No CV provided")
    retrieved_jobs = state.get("retrieved_jobs", [])
    job_matches = state.get("job_matches", [])

    # --- 2. MECHANICAL SAFETY CHECKS ---
    # Check for Forbidden Topics in the query and CV
    combined_input = (user_query + " " + cv_input).lower()
    forbidden_found = check_forbidden_content(combined_input, FORBIDDEN_TOPICS)
    if forbidden_found:
        issues.append(f"Forbidden topics detected: {', '.join(forbidden_found)}")

    # Check for Hallucinations in the Job Recommendation
    if job_matches:
        recommended_title = job_matches[0].get("title", "Unknown")
        if check_hallucination(recommended_title, retrieved_jobs):
            issues.append(f"Hallucination: Job '{recommended_title}' not found in database.")

    # --- 3. SAFETY REPORTING & LOGGING ---
    state["safety_report"] = {
        "status": "FAIL" if issues else "PASS",
        "issues": issues
    }
    
    # Log the event for your final project report
    log_safety_event(state)

    # --- 4. FINAL OUTPUT GENERATION (The 'Cleaned' Version of your friend's code) ---
    if state["safety_report"]["status"] == "FAIL":
        # Refusal message if safety check failed
        state["final_response"] = (
            f"{SAFETY_MESSAGES['failure_msg']}\n\n"
            f"Safety Issues Identified: {', '.join(issues)}"
        )
    else:
        # Success: Build the "CareerPilot Analysis" report
        recommended_job = (
            job_matches[0]["title"] if job_matches else "No suitable job found."
        )
        skill_gaps_text = (
            ", ".join(state.get("skill_gaps", [])) if state.get("skill_gaps") else "None identified."
        )
        
        # Formatting the interview questions list
        questions = state.get("interview_questions", [])
        questions_text = (
            "\n".join([f"{i + 1}. {q}" for i, q in enumerate(questions)])
            if questions else "No questions generated."
        )

        # The final formatted string
        state["final_response"] = f"""
CareerPilot Analysis

Target Role: {state.get("target_role", "Not specified")}

Recommended Job:
{recommended_job}

Skill Gaps:
{skill_gaps_text}

Interview Questions:
{questions_text}

Safety Status:
{state["safety_report"]["status"]}
{SAFETY_MESSAGES['ai_disclaimer']}
"""
    
    return state