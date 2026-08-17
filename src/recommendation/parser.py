import json
import re
from typing import Dict, Any

def parse_llm_response(response_text: str) -> Dict[str, Any]:
    """
    Parses the JSON response from the LLM, handling potential markdown formatting.
    """
    text = response_text.strip()
    
    # Strip markdown fences if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n", "", text)
        text = re.sub(r"\n```$", "", text)
        
    try:
        data = json.loads(text)
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Raw text: {text}")
        raise ValueError("LLM response is not valid JSON")

from typing import List

def validate_recommendations(parsed_data: Dict[str, Any], candidates: List[Dict]) -> Dict[str, Any]:
    """
    Guardrail: keep only restaurants whose names exist in candidate set.
    """
    valid_names = {c['restaurant_name'].strip().lower() for c in candidates}
    
    recs = parsed_data.get("recommendations", [])
    valid_recs = []
    for rec in recs:
        name = rec.get("restaurant_name", "").strip().lower()
        if name in valid_names:
            valid_recs.append(rec)
        else:
            print(f"Guardrail trigger: Dropping hallucinated restaurant '{name}'")
            
    parsed_data["recommendations"] = sorted(valid_recs, key=lambda x: x.get("rank", 999))
    return parsed_data
