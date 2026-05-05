def _normalize_text_items(items, preferred_keys=None):
    """
    Converts mixed output formats into a clean list of lowercase strings.

    Supported formats:
    - ["Data Analyst Intern", "ML Intern"]
    - [{"title": "Data Analyst Intern"}, {"skill": "SQL"}]
    """

    if preferred_keys is None:
        preferred_keys = []

    normalized_items = []

    for item in items:
        if isinstance(item, dict):
            value = ""

            for key in preferred_keys:
                if item.get(key):
                    value = item.get(key)
                    break

            if not value:
                value = str(item)

        else:
            value = str(item)

        value = value.lower().strip()

        if value:
            normalized_items.append(value)

    return normalized_items


def calculate_overlap_score(predicted_items, expected_items):
    if not expected_items:
        return 0.0

    predicted_set = set(_normalize_text_items(predicted_items))
    expected_set = set(_normalize_text_items(expected_items))

    matches = predicted_set.intersection(expected_set)
    return round(len(matches) / len(expected_set), 2)


def top_k_job_relevance(predicted_jobs, expected_jobs, k=3):
    top_jobs = predicted_jobs[:k]

    predicted_titles = _normalize_text_items(
        top_jobs,
        preferred_keys=["title", "job_title", "role"]
    )

    return calculate_overlap_score(predicted_titles, expected_jobs)


def skill_gap_correctness(predicted_skills, expected_skills):
    predicted_skill_names = _normalize_text_items(
        predicted_skills,
        preferred_keys=["skill", "name", "title"]
    )

    return calculate_overlap_score(predicted_skill_names, expected_skills)


def interview_question_relevance(questions, target_role):
    if not questions:
        return 0.0

    normalized_questions = _normalize_text_items(
        questions,
        preferred_keys=["question", "text"]
    )

    if not normalized_questions:
        return 0.0

    target_words = set(target_role.lower().split())
    relevant_count = 0

    for question in normalized_questions:
        question_words = set(question.split())
        if target_words.intersection(question_words):
            relevant_count += 1

    return round(relevant_count / len(normalized_questions), 2)


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

def intrinsic_quality_score(questions):
    if not questions:
        return 0.0

    score = 0

    # 1. Minimum length
    if all(len(q.split()) > 5 for q in questions):
        score += 0.3

    # 2. Question format
    if all("?" in q for q in questions):
        score += 0.3

    # 3. Diversity
    unique_questions = len(set(questions))
    diversity = unique_questions / len(questions)
    score += 0.4 * diversity

    return round(score, 2)