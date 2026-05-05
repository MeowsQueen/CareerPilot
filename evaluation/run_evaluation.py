from agents.workflow import build_graph
from evaluation.evaluator import (
    load_test_profiles,
    evaluate_single_output,
    calculate_average_scores,
)


def build_initial_state(profile):
    return {
        "user_query": f"I uploaded my CV and I want recommendations for {profile['target_role']}.",
        "cv_text": profile["student_background"],
        "target_role": profile["target_role"],
        "plan": {},
        "cv_profile": {},
        "retrieved_jobs": [],
        "job_matches": [],
        "skill_gaps": [],
        "interview_questions": [],
        "final_response": "",
        "safety_report": {}
    }


def run_evaluation():
    app = build_graph()
    profiles = load_test_profiles()
    results = []

    for profile in profiles:
        initial_state = build_initial_state(profile)
        agent_output = app.invoke(initial_state)

        result = evaluate_single_output(agent_output, profile)
        results.append(result)

        print("\nProfile:", profile["profile_id"])
        print(result)

    print("\nAverage Scores:")
    print(calculate_average_scores(results))


if __name__ == "__main__":
    run_evaluation()