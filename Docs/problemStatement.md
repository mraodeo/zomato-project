# Problem Statement: AI-Powered Restaurant Recommendation System (Zomato Use Case)

## Project Overview

Build an AI-powered restaurant recommendation service inspired by Zomato. The system intelligently suggests restaurants based on user preferences by combining structured data with a Large Language Model (LLM).

## Objective

Design and implement an application that:

- Takes user preferences (such as location, budget, cuisine, and ratings)
- Uses a real-world dataset of restaurants
- Leverages an LLM to generate personalized, human-like recommendations
- Displays clear and useful results to the user

## System Workflow

### 1. Data Ingestion

- Load and preprocess the Zomato dataset from Hugging Face:  
  [https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- Extract relevant fields such as:
  - Restaurant name
  - Location
  - Cuisine
  - Cost
  - Rating
  - Other useful attributes as available

### 2. User Input

Collect user preferences:

- **Location** (e.g., Delhi, Bangalore)
- **Budget** (low, medium, high)
- **Cuisine** (e.g., Italian, Chinese)
- **Minimum rating**
- **Additional preferences** (e.g., family-friendly, quick service)

### 3. Integration Layer

- Filter and prepare relevant restaurant data based on user input
- Pass structured results into an LLM prompt
- Design a prompt that helps the LLM reason and rank options

### 4. Recommendation Engine

Use the LLM to:

- Rank restaurants
- Provide explanations (why each recommendation fits)
- Optionally summarize choices

### 5. Output Display

Present top recommendations in a user-friendly format:

| Field                    | Description                          |
|--------------------------|--------------------------------------|
| Restaurant Name          | Name of the recommended restaurant   |
| Cuisine                  | Type(s) of cuisine offered           |
| Rating                   | Restaurant rating                    |
| Estimated Cost           | Approximate cost / budget category   |
| AI-generated explanation | Why this restaurant matches the user |

## Success Criteria

- Accurate filtering of restaurants from the real-world dataset based on user constraints
- Effective LLM prompting that produces ranked, personalized recommendations
- Clear, human-readable explanations for each suggestion
- End-to-end flow from data load → user input → filtered candidates → LLM ranking → displayed results

## Dataset

- **Source:** Hugging Face  
- **Dataset:** `ManikaSaini/zomato-restaurant-recommendation`  
- **URL:** https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation

## Tech Context

- **Dataset source:** Hugging Face (`ManikaSaini/zomato-restaurant-recommendation`)
- **Core AI component:** Large Language Model for ranking and explanation generation
- **Application style:** Preference-driven recommendation service (Zomato-inspired)