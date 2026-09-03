import os
from google import genai


def get_ai_feedback(twin, recommendations):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Error: GEMINI_API_KEY is not configured."

    client = genai.Client(api_key=api_key)

    recommendation_text = "\n".join(
        [
            f"- {r['skill']}: {r['message']}"
            for r in recommendations
        ]
    )

    prompt = f"""
You are StudyTwin, an intelligent AI programming mentor.

Analyze this developer's coding profile:

Debugging Score: {twin['debugging']}/100
Complexity Score: {twin['complexity']}/100
Total Submissions: {twin['submissions']}

Current Recommendations:
{recommendation_text}

Give personalized feedback with these sections:

1. Developer Strength
2. Main Weakness
3. Why This Matters
4. What To Learn Next
5. Practice Challenge

Keep the response concise, beginner-friendly, and motivating.
"""

    try:
        interaction = client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt
        )

        return interaction.output_text

    except Exception as e:
        return f"AI Mentor Error: {str(e)}"