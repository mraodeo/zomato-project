Creating a detailed `architecture.md` from the problem statement context.

```markdown
# Architecture Document
## AI-Powered Restaurant Recommendation System (Zomato Use Case)

---

## 1. Introduction

### 1.1 Purpose
This document defines the system architecture for an AI-powered restaurant recommendation service inspired by Zomato. It describes components, data flow, integration points, and design decisions required to turn user preferences into personalized, LLM-explained restaurant recommendations.

### 1.2 Scope
The system will:
- Ingest and preprocess a real-world Zomato restaurant dataset from Hugging Face
- Accept user preferences (location, budget, cuisine, rating, additional needs)
- Filter structured restaurant data against those preferences
- Use an LLM to rank candidates and generate human-like explanations
- Present top recommendations in a clear, user-friendly format

### 1.3 Goals
- Accurate preference-based filtering on real restaurant data
- High-quality, explainable LLM recommendations
- Modular design so data, logic, and model layers can evolve independently
- Simple end-to-end path from input → results

### 1.4 Non-Goals (Initial Version)
- Real-time booking or order placement
- Live Zomato API integration
- User accounts, history, or collaborative filtering
- Mobile native apps
- Multi-city live inventory or pricing sync

---

## 2. High-Level Architecture

The system follows a **layered pipeline architecture**: Data → Input → Filter/Integration → LLM Recommendation → Presentation.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Presentation Layer                       │
│          (CLI / Web UI / API response formatting)               │
└────────────────────────────▲────────────────────────────────────┘
                             │ Top-N recommendations + explanations
┌────────────────────────────┴────────────────────────────────────┐
│                   Recommendation Engine (LLM)                   │
│        Ranking │ Explanations │ Optional summary                │
└────────────────────────────▲────────────────────────────────────┘
                             │ Structured prompt + candidate set
┌────────────────────────────┴────────────────────────────────────┐
│                       Integration Layer                         │
│     Preference filtering │ Candidate prep │ Prompt builder      │
└────────────────────────────▲────────────────────────────────────┘
                             │ User preferences + raw/cleaned data
┌────────────────────────────┴────────────────────────────────────┐
│                     Application / Input Layer                   │
│              Collect & validate user preferences                │
└────────────────────────────▲────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                        Data Layer                               │
│     Hugging Face dataset load │ Clean │ Normalize │ Cache       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. System Components

### 3.1 Data Ingestion Module
**Responsibility:** Load, clean, and normalize the Zomato dataset.

| Aspect | Detail |
|--------|--------|
| Source | `ManikaSaini/zomato-restaurant-recommendation` (Hugging Face) |
| Operations | Download/load, schema selection, missing-value handling, type normalization |
| Output | Clean tabular dataset (in-memory DataFrame and/or local cache) |

**Relevant fields (logical model):**
- `restaurant_name`
- `location` / `city`
- `cuisine`
- `cost` (average cost for two or equivalent)
- `rating`
- Optional: votes, online order, table booking, address, rest_type, dishes, etc.

**Design notes:**
- Prefer one-time load + local cache (e.g. Parquet/CSV) for faster iteration
- Normalize location and cuisine for case-insensitive matching
- Map numeric cost into budget bands: `low` | `medium` | `high`

---

### 3.2 User Input Module
**Responsibility:** Collect and validate preference inputs.

**Input schema:**

| Field | Type | Example | Required |
|-------|------|---------|----------|
| `location` | string | `"Bangalore"` | Yes |
| `budget` | enum | `"low"` \| `"medium"` \| `"high"` | Yes |
| `cuisine` | string | `"Italian"` | Yes |
| `min_rating` | float | `4.0` | Yes |
| `additional_preferences` | string | `"family-friendly, quick service"` | No |
| `top_n` | int | `5` | No (default: 5) |

**Validation rules:**
- Reject empty location/cuisine when required
- Clamp `min_rating` to valid range (e.g. 0–5)
- Normalize enums and strings (trim, title-case/lowercase as needed)

---

### 3.3 Integration Layer
**Responsibility:** Bridge structured data and the LLM.

**Subcomponents:**

1. **Filter Engine**
   - Apply deterministic filters:
     - Location match (exact or contains)
     - Cuisine match (substring / token match)
     - Rating ≥ `min_rating`
     - Cost within selected budget band
   - Limit candidate set size (e.g. top 20–50 by rating) to control prompt size/cost

2. **Candidate Serializer**
   - Convert filtered rows into compact structured text/JSON for the prompt
   - Include only fields useful for ranking and explanation

3. **Prompt Builder**
   - System instructions: role, ranking criteria, output format
   - User preferences block
   - Candidate restaurants block
   - Output contract (e.g. ranked list + explanation per item)

**Filtering flow:**

```
User Preferences
      │
      ▼
┌──────────────┐     ┌────────────────┐     ┌────────────────────┐
│ Location     │────►│ Cuisine filter │────►│ Rating + Budget    │
│ filter       │     │                │     │ filter             │
└──────────────┘     └────────────────┘     └─────────┬──────────┘
                                                      │
                                                      ▼
                                            Candidate Set (K items)
                                                      │
                                                      ▼
                                               Prompt Builder
```

---

### 3.4 Recommendation Engine (LLM)
**Responsibility:** Rank filtered restaurants and generate explanations.

**Capabilities:**
- Rank candidates by fit to user preferences
- Explain *why* each recommendation matches
- Optionally produce a short overall summary
- Stay within provided candidates (no hallucinated restaurants)

**LLM interface (logical):**

```text
Input:
  - system_prompt
  - user_preferences
  - candidate_restaurants[]

Output:
  - recommendations[]:
      - rank
      - restaurant_name
      - cuisine
      - rating
      - estimated_cost
      - explanation
  - optional_summary
```

**Design guidelines:**
- Temperature low–medium for more consistent ranking
- Strict JSON (or clearly delimited) output for reliable parsing
- Explicit instruction: only recommend from the candidate list
- Tie-break guidance: higher rating, closer budget fit, richer cuisine match, then additional preferences

---

### 3.5 Output / Presentation Layer
**Responsibility:** Display final recommendations clearly.

**Output card per restaurant:**
- Restaurant Name
- Cuisine
- Rating
- Estimated Cost
- AI-generated explanation

**Channels (implementation options):**
- CLI / terminal tables
- Streamlit / Gradio web UI
- REST API JSON response
- Notebook demo

---

## 4. End-to-End Data Flow

```
1. Startup / first request
   └─ Load dataset from Hugging Face (or local cache)
   └─ Preprocess & normalize fields
   └─ Optionally build indexes (location, cuisine)

2. User submits preferences
   └─ Validate input schema

3. Integration layer
   └─ Filter dataset → candidate set (K restaurants)
   └─ If no candidates: return empty-state message (skip LLM or ask LLM to suggest relaxation)
   └─ Serialize candidates + build prompt

4. LLM recommendation
   └─ Call LLM with prompt
   └─ Parse structured response
   └─ Validate names against candidate set (guardrail)

5. Presentation
   └─ Format Top-N recommendations
   └─ Show explanations (+ optional summary)
```

---

## 5. Prompt Architecture

### 5.1 Prompt Structure
1. **Role:** Expert restaurant recommendation assistant (Zomato-like)
2. **Objective:** Rank candidates and explain fit
3. **User preferences:** location, budget, cuisine, min rating, extras
4. **Candidates:** compact list/JSON of allowed restaurants
5. **Rules:**
   - Use only provided candidates
   - Respect hard filters already applied
   - Optimize for preference fit + quality
   - Return strict structured output
6. **Output schema:** ranked recommendations + explanations

### 5.2 Example Output Contract (JSON)

```json
{
  "summary": "Short overview of the picks",
  "recommendations": [
    {
      "rank": 1,
      "restaurant_name": "Example Cafe",
      "cuisine": "Italian",
      "rating": 4.5,
      "estimated_cost": "medium",
      "explanation": "Matches Italian cuisine in Bangalore with strong rating and mid-range pricing; suitable for families."
    }
  ]
}
```

---

## 6. Budget Mapping Strategy

Because users choose qualitative budget levels, map dataset cost to bands:

| Budget | Logical rule (configurable) |
|--------|-----------------------------|
| `low` | cost ≤ 33rd percentile OR cost ≤ threshold_L |
| `medium` | between low and high thresholds |
| `high` | cost ≥ 66th percentile OR cost ≥ threshold_H |

Thresholds should be derived from dataset distribution (especially per city if available).

---

## 7. Technology Stack (Recommended)

| Layer | Suggested options |
|-------|-------------------|
| Language | Python 3.10+ |
| Data loading | `datasets` (Hugging Face), `pandas` |
| Validation | Pydantic models |
| LLM access | OpenAI API / Azure OpenAI / Anthropic / local model via compatible API |
| Prompt orchestration | LangChain or direct SDK calls (keep thin) |
| API (optional) | FastAPI |
| UI (optional) | Streamlit or Gradio |
| Config | `.env` + `pydantic-settings` |
| Caching | Local Parquet/CSV cache for dataset |

---

## 8. Logical Module Structure

```text
restaurant-recommender/
├── docs/
│   ├── problemStatement.md
│   └── architecture.md
├── data/
│   └── cache/                  # processed dataset cache
├── src/
│   ├── __init__.py
│   ├── config.py               # settings, thresholds, model names
│   ├── data/
│   │   ├── loader.py           # HF load + cache
│   │   ├── preprocess.py       # clean/normalize/budget bands
│   │   └── schema.py           # column mapping
│   ├── input/
│   │   └── preferences.py      # preference model + validation
│   ├── integration/
│   │   ├── filter.py           # deterministic filters
│   │   ├── serializer.py       # candidates → prompt-friendly structure
│   │   └── prompt_builder.py   # system/user prompt assembly
│   ├── recommendation/
│   │   ├── llm_client.py       # LLM API wrapper
│   │   ├── engine.py           # rank + explain orchestration
│   │   └── parser.py           # parse/validate LLM output
│   ├── presentation/
│   │   ├── formatter.py        # tables/cards/JSON
│   │   └── app_streamlit.py    # optional UI
│   └── main.py                 # CLI or app entry
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

---

## 9. API Design (Optional REST Layer)

### `POST /api/v1/recommendations`

**Request:**
```json
{
  "location": "Delhi",
  "budget": "medium",
  "cuisine": "Chinese",
  "min_rating": 4.0,
  "additional_preferences": "quick service",
  "top_n": 5
}
```

**Response:**
```json
{
  "query": { "...": "echoed preferences" },
  "candidate_count": 27,
  "summary": "Best mid-budget Chinese options in Delhi with strong ratings.",
  "recommendations": [
    {
      "rank": 1,
      "restaurant_name": "Dragon House",
      "cuisine": "Chinese",
      "rating": 4.3,
      "estimated_cost": "medium",
      "explanation": "..."
    }
  ]
}
```

**Error cases:**
- `400` invalid input
- `404` no restaurants match filters
- `502` LLM upstream failure
- `500` unexpected server error

---

## 10. Non-Functional Architecture

### 10.1 Performance
- Cache preprocessed dataset on disk/memory
- Cap candidates sent to LLM (token & latency control)
- Optional request timeouts on LLM calls

### 10.2 Reliability
- Graceful empty-result handling before LLM call
- Parse fallback if LLM output is malformed (retry with repair prompt once)
- Guardrail: drop recommendations not in candidate set

### 10.3 Security & Privacy
- No persistent storage of personal user profiles in v1
- API keys only via environment variables
- Sanitize user free-text before inserting into prompts

### 10.4 Cost Control
- Deterministic pre-filtering to reduce tokens
- Configurable `top_n` and max candidates
- Choose compact prompt serialization

### 10.5 Observability
- Log: filter counts, latency, token usage (if available), parse failures
- Avoid logging full secrets or raw API keys

---

## 11. Guardrails & Edge Cases

| Scenario | Handling |
|----------|----------|
| No candidates after filtering | Return helpful message; suggest relaxing rating/budget/cuisine |
| Multiple cuisine values in dataset | Tokenize on commas/slashes; match any token |
| Missing cost/rating values | Exclude from filtered set or impute conservatively |
| LLM hallucinated restaurant | Filter out by name match against candidates |
| Ambiguous location | Prefer city-level contains match; optional fuzzy match later |
| Very large candidate set | Pre-sort by rating and truncate to K |

---

## 12. Architectural Decisions (ADR Summary)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Hybrid retrieval + LLM | Deterministic filter, then LLM rank/explain | Accuracy + explainability; lower hallucination risk |
| Dataset source | Hugging Face Zomato dataset | Matches problem statement; reproducible |
| Budget model | Qualitative bands mapped from cost | User-friendly and aligned with requirements |
| Output style | Structured recommendations + explanations | Clear UX and machine-parseable results |
| Modular layers | Data / Input / Integration / LLM / Presentation | Testable and extensible |

---

## 13. Future Extensions
- Embeddings + vector search for semantic cuisine/preference match
- User session memory and personalization
- Map/geo distance filtering
- Multi-turn chat refinement (“cheaper”, “more romantic”)
- A/B testing of prompt variants
- Deployment: Docker + cloud API + simple web frontend

---

## 14. Success Metrics (Architecture Alignment)

- **Functional:** End-to-end flow works from preferences → top recommendations with explanations  
- **Relevance:** Filtered candidates satisfy hard constraints (location, budget, cuisine, rating)  
- **Faithfulness:** LLM outputs only valid candidate restaurants  
- **UX:** Results show name, cuisine, rating, cost, and clear AI explanation  
- **Operability:** Dataset cached; LLM failures handled gracefully  

---

## 15. Alignment with Problem Statement Workflow

| Problem Statement Stage | Architecture Mapping |
|-------------------------|----------------------|
| 1. Data Ingestion | Data Layer (`loader`, `preprocess`) |
| 2. User Input | Input Module (`preferences`) |
| 3. Integration Layer | Filter + Serializer + Prompt Builder |
| 4. Recommendation Engine | LLM client + ranking/explanation engine |
| 5. Output Display | Presentation/formatter/UI/API |

---

## 16. Summary

This architecture implements a **hybrid recommendation pipeline**: structured data filtering for precision, and an LLM for ranking and human-like explanations. Clear module boundaries keep the system maintainable, testable, and ready for CLI, API, or UI delivery while fully satisfying the Zomato-inspired problem statement.
```

**How to save**
1. Copy the content above  
2. Save as `docs/architecture.md`  
(or `architecture.md` in the project root)

This doc covers components, data flow, prompt design, stack, module layout, API shape, guardrails, and alignment with your problem statement. I can next generate `implementation-plan.md` or scaffold the `src/` module structure if you want.