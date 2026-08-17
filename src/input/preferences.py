from typing import Optional
from typing_extensions import Literal
from pydantic import BaseModel, Field, validator

class UserPreferences(BaseModel):
    location: str = Field(..., description="City or location to search for restaurants")
    budget: Literal["low", "medium", "high"] = Field(..., description="Budget band")
    cuisine: str = Field(..., description="Preferred cuisine")
    min_rating: float = Field(0.0, ge=0.0, le=5.0, description="Minimum acceptable rating")
    additional_preferences: Optional[str] = Field(None, description="Any other preferences")
    top_n: int = Field(5, ge=1, le=10, description="Number of recommendations to return")

    @validator("location")
    @classmethod
    def validate_non_empty_string(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty")
        return v
    
    @validator("budget")
    @classmethod
    def validate_budget_case(cls, v: str) -> str:
        return v.lower()
