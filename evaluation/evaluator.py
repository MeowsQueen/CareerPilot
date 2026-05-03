import json
from pathlib import Path

from evaluation.metrics import (
    top_k_job_relevance,
    skill_gap_correctness,
    interview_question_relevance,
    response_completeness,
)


def load_test_profiles(folder_path="evaluation/test_profiles"):
    profiles = []

    for file_path in Path(folder_path).glob("profile_*.json"):
        with open(file_path, "r", encoding="utf-8") as file:
            profiles.append(json.load(file))

    return profiles


def evaluate_single_output(agent_output, expected_profile):
    return {
        "profile_id": expected_profile.get("profile_id"),
        "target_role": expected_profile.get("target_role"),
        "job_match_score": top_k_job_relevance(
            agent_output.get("job_matches", []),
            expected_profile.get("expected_jobs", []),
            k=3,
        ),
        "skill_gap_score": skill_gap_correctness(
            agent_output.get("skill_gaps", []),
            expected_profile.get("expected_skill_gaps", []),
        ),
        "interview_question_score": interview_question_relevance(
            agent_output.get("interview_questions", []),
            expected_profile.get("target_role", ""),
        ),
        "response_completeness": response_completeness(agent_output),
    }


def calculate_average_scores(results):
    if not results:
        return {}

    metric_keys = [
        "job_match_score",
        "skill_gap_score",
        "interview_question_score",
        "response_completeness",
    ]

    averages = {}

    for key in metric_keys:
        averages[key] = round(
            sum(result[key] for result in results) / len(results),
            2,
        )

    return averages


if __name__ == "__main__":
    print("Evaluation module is ready.")
    print("Run this module after connecting real CareerPilot outputs.")