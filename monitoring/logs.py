import datetime
import os

def log_safety_event(state):
    """
    Records the outcome of a safety check into a local text file.
    """
    report = state.get("safety_report", {})
    status = report.get("status", "UNKNOWN")
    issues = report.get("issues", [])
    query = state.get("user_query", "No query found")

    # Define the log path
    log_file = "monitoring/safety_logs.txt"

    # Create a timestamped entry
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] STATUS: {status} | "
        f"QUERY: {query[:50]}... | "
        f"ISSUES: {issues}\n"
    )

    # Append to the file (creates it if it doesn't exist)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)