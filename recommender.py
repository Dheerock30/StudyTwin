def generate_recommendations(twin):

    recommendations = []

    if twin["debugging"] < 50:

        recommendations.append({
            "skill": "Debugging",
            "priority": "High",
            "message": (
                "Practice reading Python errors, tracebacks, "
                "and understanding exceptions."
            )
        })

    elif twin["debugging"] < 75:

        recommendations.append({
            "skill": "Debugging",
            "priority": "Medium",
            "message": (
                "Review common Python errors and debugging techniques."
            )
        })

    if twin["complexity"] < 50:

        recommendations.append({
            "skill": "Complexity",
            "priority": "High",
            "message": (
                "Learn Big-O notation and practice reducing "
                "deeply nested loops."
            )
        })

    elif twin["complexity"] < 75:

        recommendations.append({
            "skill": "Complexity",
            "priority": "Medium",
            "message": (
                "Practice identifying O(n²) patterns and "
                "finding more efficient solutions."
            )
        })

    if not recommendations:

        recommendations.append({
            "skill": "Overall",
            "priority": "Low",
            "message": (
                "Your current code patterns look strong. "
                "Try solving more challenging problems."
            )
        })

    return recommendations