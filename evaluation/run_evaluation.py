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


def print_agent_output(agent_output):
    print("\nCareerPilot Output")
    print("-" * 40)

    job_matches = agent_output.get("job_matches", [])
    skill_gaps = agent_output.get("skill_gaps", [])
    interview_questions = agent_output.get("interview_questions", [])
    final_response = agent_output.get("final_response", "")
    safety_report = agent_output.get("safety_report", {})

    if job_matches:
        print("\nRecommended Jobs:")
        for index, job in enumerate(job_matches, start=1):
            if isinstance(job, dict):
                print(f"{index}. {job.get('title', 'Unknown Job')}")
                print(f"   Match Score: {job.get('match_score', 'N/A')}")
                print(f"   Reason: {job.get('match_reason', 'N/A')}")
            else:
                print(f"{index}. {job}")
    else:
        print("\nRecommended Jobs: No job matches returned.")

    if skill_gaps:
        print("\nSkill Gaps:")
        for skill in skill_gaps:
            print(f"- {skill}")
    else:
        print("\nSkill Gaps: No skill gaps returned.")

    if interview_questions:
        print("\nInterview Questions:")
        for index, question in enumerate(interview_questions, start=1):
            print(f"{index}. {question}")
    else:
        print("\nInterview Questions: No interview questions returned.")

    if safety_report:
        print("\nSafety Report:")
        print(safety_report)

    if final_response:
        print("\nFinal Response:")
        print(final_response)


def run_evaluation():
    app = build_graph()
    profiles = load_test_profiles()
    results = []

    for profile in profiles:
        print("\n" + "=" * 60)
        print(f"Profile: {profile['profile_id']}")
        print(f"Target Role: {profile['target_role']}")
        print("=" * 60)

        initial_state = build_initial_state(profile)
        agent_output = app.invoke(initial_state)

        print_agent_output(agent_output)

        result = evaluate_single_output(agent_output, profile)
        results.append(result)

        print("\nEvaluation Scores:")
        print(result)

    print("\n" + "=" * 60)
    print("Average Evaluation Scores")
    print("=" * 60)
    print(calculate_average_scores(results))


if __name__ == "__main__":
    run_evaluation()