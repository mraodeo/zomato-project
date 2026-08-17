import argparse
from typing import Optional
from src.input.preferences import UserPreferences
from pydantic import ValidationError

def collect_preferences_cli() -> Optional[UserPreferences]:
    """Collects user preferences from CLI arguments or interactive prompts."""
    parser = argparse.ArgumentParser(description="Restaurant Recommendation Engine")
    parser.add_argument("--location", type=str, help="City or location")
    parser.add_argument("--budget", type=str, choices=["low", "medium", "high"], help="Budget band")
    parser.add_argument("--cuisine", type=str, help="Preferred cuisine")
    parser.add_argument("--min_rating", type=float, help="Minimum acceptable rating (0-5)")
    parser.add_argument("--additional", type=str, help="Additional preferences")
    parser.add_argument("--top_n", type=int, help="Number of recommendations to return")
    
    args, unknown = parser.parse_known_args()
    
    # If any required arg is missing, fallback to interactive prompts
    try:
        location = args.location or input("Enter location (e.g., Delhi): ").strip()
        budget = args.budget or input("Enter budget (low/medium/high): ").strip().lower()
        cuisine = args.cuisine or input("Enter preferred cuisine (e.g., North Indian, Chinese): ").strip()
        
        min_rating_str = str(args.min_rating) if args.min_rating else input("Enter minimum rating (0-5) [0]: ").strip()
        min_rating = float(min_rating_str) if min_rating_str else 0.0
        
        additional = args.additional or input("Any additional preferences? (optional): ").strip()
        additional = additional if additional else None
        
        top_n_str = str(args.top_n) if args.top_n else input("Number of recommendations [5]: ").strip()
        top_n = int(top_n_str) if top_n_str else 5
        
        prefs = UserPreferences(
            location=location,
            budget=budget,
            cuisine=cuisine,
            min_rating=min_rating,
            additional_preferences=additional,
            top_n=top_n
        )
        return prefs
    except ValidationError as e:
        print("\nInvalid input. Please check your answers:")
        for error in e.errors():
            print(f"- {error['loc'][0]}: {error['msg']}")
        return None
    except ValueError:
        print("\nInvalid numeric input provided.")
        return None
