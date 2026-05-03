# Evaluation Rubric

This evaluation module measures the performance of the CareerPilot multi-agent system using predefined student profiles.

## 1. Job Match Relevance

This metric evaluates whether the recommended jobs match the expected target roles for a given student profile.

Scoring:
- 1.00: All expected job roles are matched.
- 0.67: Two relevant matches are found.
- 0.33: One relevant match is found.
- 0.00: No relevant match is found.

## 2. Skill Gap Correctness

This metric evaluates whether the system correctly identifies missing skills based on the target role and student profile.

Scoring:
- 1.00: All expected missing skills are identified.
- 0.67: Most missing skills are identified.
- 0.33: Some missing skills are identified.
- 0.00: No relevant missing skill is identified.

## 3. Interview Question Relevance

This metric evaluates whether generated interview questions are relevant to the selected target role.

Scoring:
- 1.00: All questions are relevant.
- 0.50: Some questions are relevant.
- 0.00: Questions are missing or irrelevant.

## 4. Response Completeness

This metric checks whether the final system output includes the required components:
- CV analysis
- Job matches
- Skill gaps
- Interview questions
- Final output

## 5. Evaluation Goal

The goal of the evaluation process is not only to measure output accuracy, but also to verify whether the multi-agent workflow produces complete, relevant, and useful career guidance.