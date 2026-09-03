def calculate_twin(history):

    if not history:
        return {
            "debugging": 0,
            "complexity": 0,
            "submissions": 0
        }

    debugging_scores = [
        row[1]
        for row in history
    ]

    complexity_scores = [
        row[2]
        for row in history
    ]

    debugging_average = round(
        sum(debugging_scores) / len(debugging_scores)
    )

    complexity_average = round(
        sum(complexity_scores) / len(complexity_scores)
    )

    return {
        "debugging": debugging_average,
        "complexity": complexity_average,
        "submissions": len(history)
    }


def get_skill_level(score):

    if score >= 80:
        return "Strong"

    elif score >= 60:
        return "Developing"

    else:
        return "Needs Improvement"