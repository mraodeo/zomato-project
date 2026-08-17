import os
from src.config import LLM_PROVIDER, LLM_MODEL, LLM_API_KEY, LLM_TEMPERATURE

try:
    import groq
    client = groq.Groq(api_key=LLM_API_KEY) if LLM_API_KEY else None
except ImportError:
    groq = None
    client = None

from typing import List, Dict

def call_llm(messages: List[Dict]) -> str:
    """
    Calls the Groq LLM API with the provided messages.
    """
    if LLM_PROVIDER.lower() != "groq":
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")
        
    if not client:
        raise ValueError("Groq API key not found or groq package not installed.")
        
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=LLM_TEMPERATURE,
        response_format={"type": "json_object"}
    )
    
    return response.choices[0].message.content

