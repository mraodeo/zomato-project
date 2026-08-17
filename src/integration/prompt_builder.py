from typing import Optional
from src.input.preferences import UserPreferences

SYSTEM_PROMPT = """You are an expert restaurant recommendation engine.
You must rank the provided candidate restaurants based on the user's preferences.
You must explain why you chose each restaurant, keeping the explanation concise (1-2 sentences).
You must only use the candidates provided in the input. Do not invent or hallucinate any restaurants.
Your response MUST be valid JSON matching the following schema:
{
  "recommendations": [
    {
      "rank": 1,
      "restaurant_name": "Name",
      "cuisine": "Cuisine",
      "rating": 4.5,
      "estimated_cost": 1000,
      "explanation": "Short explanation here."
    }
  ],
  "summary": "Overall summary of your picks."
}"""

from typing import List, Dict

def build_prompt(preferences: UserPreferences, candidates_json: str) -> List[Dict]:
    """
    Builds the chat messages array for the LLM.
    """
    user_content = f"""USER PREFERENCES:
- Location: {preferences.location}
- Cuisine: {preferences.cuisine}
- Budget: {preferences.budget}
- Min Rating: {preferences.min_rating}
- Additional Preferences: {preferences.additional_preferences or 'None'}
- Top N recommendations: {preferences.top_n}

CANDIDATES:
{candidates_json}

INSTRUCTIONS:
Rank the top {preferences.top_n} restaurants from the CANDIDATES list above that best match the USER PREFERENCES.
Return the result in strictly valid JSON format."""
    
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content}
    ]

def get_empty_set_response() -> dict:
    """
    Returns a structured 'no match' result when no candidates are found.
    """
    return {
        "recommendations": [],
        "summary": "No matching restaurants were found based on your exact preferences. Consider relaxing your constraints (e.g., lower the minimum rating or change the budget band)."
    }
