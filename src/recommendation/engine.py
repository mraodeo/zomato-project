from typing import Dict, Any
import pandas as pd
from src.input.preferences import UserPreferences
from src.integration.serializer import serialize_candidates
from src.integration.prompt_builder import build_prompt, get_empty_set_response
from src.recommendation.llm_client import call_llm
from src.recommendation.parser import parse_llm_response, validate_recommendations

def fallback_recommendation(candidates_df: pd.DataFrame, preferences: UserPreferences) -> Dict[str, Any]:
    """
    Deterministic fallback if LLM fails.
    """
    top_candidates = candidates_df.head(preferences.top_n).to_dict(orient='records')
    recs = []
    for i, c in enumerate(top_candidates):
        recs.append({
            "rank": i + 1,
            "restaurant_name": c.get("restaurant_name", "Unknown"),
            "cuisine": c.get("cuisine", "Unknown"),
            "rating": c.get("rating", 0.0),
            "estimated_cost": c.get("cost", 0.0),
            "explanation": f"Fallback: Top rated {c.get('cuisine', '')} restaurant in {c.get('location', '')} matching your budget."
        })
    return {
        "summary": "LLM failed or API key missing. Showing deterministic top-rated matches.",
        "recommendations": recs
    }

def recommend(preferences: UserPreferences, candidates_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Orchestrate: preferences + candidates -> prompt -> LLM -> parse -> guardrails
    """
    if candidates_df.empty:
        return get_empty_set_response()
        
    candidates_json = serialize_candidates(candidates_df)
    messages = build_prompt(preferences, candidates_json)
    
    try:
        response_text = call_llm(messages)
        parsed_data = parse_llm_response(response_text)
    except Exception as e:
        print(f"LLM call/parse failed: {e}")
        # Deterministic fallback
        return fallback_recommendation(candidates_df, preferences)
        
    # Convert candidates DataFrame to list of dicts for guardrail check
    candidates_list = candidates_df.to_dict(orient='records')
    validated_data = validate_recommendations(parsed_data, candidates_list)
    
    # Slice to top_n
    validated_data["recommendations"] = validated_data["recommendations"][:preferences.top_n]
    
    return validated_data
