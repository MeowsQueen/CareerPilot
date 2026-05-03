def calculate_overlap_score(predicted_items, expected_items):
    if not expected_items:
        return 0.0

    predicted_set = set(item.lower().strip() for item in predicted_items)
    expected_set = set(item.lower().strip() for item in expected_items)

    matches = predicted_set.intersection(expected_set)
    return round(len(matches) / len(expected_set), 2)


def top_k_job_relevance(predicted_jobs, expected_jobs, k=3):
    top_jobs = predicted_jobs[:k]
    return calculate_overlap_score(top_jobs, expected_jobs)


def skill_gap_correctness(predicted_skills, expected_skills):
    return calculate_overlap_score(predicted_skills, expected_skills)


def interview_question_relevance(questions, target_role):
    if not questions:
        return 0.0

    target_words = set(target_role.lower().split())
    relevant_count = 0

    for question in questions:
        question_words = set(question.lower().split())
        if target_words.intersection(question_words):
            relevant_count += 1

    return round(relevant_count / len(questions), 2)


def response_completeness(output):
    required_fields = [
        "cv_profile",
        "job_matches",
        "skill_gaps",
        "interview_questions",
        "final_response",
        "safety_report"
    ]

    completed = 0
    for field in required_fields:
        if output.get(field):
            completed += 1

    return round(completed / len(required_fields), 2)
   