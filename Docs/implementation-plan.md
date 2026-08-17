Creating a phase-wise `implementation-plan.md` aligned with the problem statement and architecture.

```markdown
# Implementation Plan
## AI-Powered Restaurant Recommendation System (Zomato Use Case)

This plan translates `docs/problemStatement.md` and `docs/architecture.md` into a phased, executable delivery roadmap.

---

## 0. Overview

### 0.1 Delivery strategy
Build in vertical slices: make each phase produce something runnable, then harden and productize.

### 0.2 Phase map

| Phase | Name | Primary outcome |
|-------|------|-----------------|
| 1 | Foundation & project setup | Repo, config, dependencies, docs alignment |
| 2 | Data ingestion & preprocessing | Clean, cached Zomato dataset ready for filtering |
| 3 | User input & validation | Preference schema and validation |
| 4 | Integration layer | Filtering, candidate prep, prompt builder |
| 5 | LLM recommendation engine | Ranked recommendations + explanations |
| 6 | API & Frontend Layer | FastAPI backend + High-quality Next.js UI (`stitch_tablemate_ai_recommendation_engine`) |
| 7 | Reliability, guardrails & testing | Edge cases, parsing safety, tests |
| 8 | Polish, docs & release | README, env samples, demo script |

### 0.3 Definition of Done (program-level)
- User can provide location, budget, cuisine, min rating, and optional preferences
- System filters real Hugging Face Zomato data
- LLM ranks candidates and explains each recommendation
- Output shows: name, cuisine, rating, estimated cost, AI explanation
- Empty results, bad LLM output, and missing fields are handled gracefully

---

## Phase 1 — Foundation & Project Setup

**Goal:** Establish a clean, reproducible project skeleton matching the architecture.

### Tasks
1. Create repository structure:
   ```text
   restaurant-recommender/
   ├── docs/
   │   ├── problemStatement.md
   │   ├── architecture.md
   │   └── implementation-plan.md
   ├── data/cache/
   ├── src/
   │   ├── config.py
   │   ├── data/
   │   ├── input/
   │   ├── integration/
   │   ├── recommendation/
   │   ├── presentation/
   │   └── main.py
   ├── stitch_tablemate_ai_recommendation_engine/
   ├── tests/
   ├── requirements.txt
   ├── .env.example
   └── README.md
   ```
2. Add Python version pin (3.10+ recommended).
3. Create `requirements.txt` with baseline deps:
   - `datasets`, `pandas`, `pydantic`, `python-dotenv`, `fastapi`, `uvicorn`
   - LLM SDK (e.g. `openai` or chosen provider)
   - Testing: `pytest`
4. Implement `src/config.py`:
   - Model name, temperature, max candidates, default `top_n`
   - Budget thresholds (placeholders)
   - Dataset id: `ManikaSaini/zomato-restaurant-recommendation`
   - Cache path
5. Add `.env.example` (`LLM_API_KEY`, `LLM_MODEL`, etc.).
6. Smoke-test virtualenv install.

### Deliverables
- [ ] Folder structure created
- [ ] Dependencies install cleanly
- [ ] Config loads from env
- [ ] Placeholder entrypoint `python -m src.main` runs

### Exit criteria
Project boots locally with no business logic yet.

---

## Phase 2 — Data Ingestion & Preprocessing

**Goal:** Load the Hugging Face dataset once, clean it, and cache a normalized table.

### Tasks
1. **Loader (`src/data/loader.py`)**
   - Load dataset via `datasets.load_dataset(...)`
   - Convert to pandas DataFrame
   - Save/load local cache (`data/cache/restaurants.parquet` or `.csv`)
2. **Schema mapping (`src/data/schema.py`)**
   - Map raw columns → logical fields:
     - `restaurant_name`, `location`, `cuisine`, `cost`, `rating`
     - optional: `votes`, `rest_type`, `address`, `online_order`, etc.
   - Handle unknown/alternate column names defensively
3. **Preprocess (`src/data/preprocess.py`)**
   - Drop critical-null rows (name/location)
   - Normalize strings (trim, case folding for match columns)
   - Parse numeric `rating` and `cost`
   - Split multi-cuisine strings into searchable form
   - Derive `budget_band` (`low` / `medium` / `high`) from cost distribution
4. **Budget banding**
   - Compute thresholds from data (global and optionally per-city)
   - Document rules in config
5. **CLI/util**
   - `load_dataset_summary()` → row count, columns, sample cities/cuisines

### Deliverables
- [ ] Cached cleaned dataset
- [ ] Documented column mapping
- [ ] Budget band distribution summary
- [ ] Unit tests for parsing/normalization helpers

### Exit criteria
`preprocess()` returns a stable DataFrame usable by filters, with required logical columns present.

### Risks & mitigations
| Risk | Mitigation |
|------|------------|
| Unexpected schema | Flexible column mapper + startup validation |
| Slow repeated HF downloads | Local cache with cache-invalidation flag |
| Sparse cost/rating | Explicit drop/impute policy logged at startup |

---

## Phase 3 — User Input & Validation

**Goal:** Collect preferences in a validated, typed structure.

### Tasks
1. Define Pydantic model (`src/input/preferences.py`):
   - `location: str`
   - `budget: Literal["low", "medium", "high"]`
   - `cuisine: str`
   - `min_rating: float`
   - `additional_preferences: Optional[str]`
   - `top_n: int = 5`
2. Validation rules:
   - Non-empty location/cuisine
   - `min_rating` in `[0, 5]`
   - `top_n` in sensible bounds (e.g. 1–10)
   - Normalize whitespace/case where useful
3. Input adapters:
   - CLI prompts / argparse
   - (Later) API JSON body / Streamlit form
4. Friendly error messages for invalid input.

### Deliverables
- [ ] `UserPreferences` model
- [ ] CLI preference collection
- [ ] Validation tests

### Exit criteria
Invalid inputs are rejected clearly; valid inputs produce a canonical preferences object.

---

## Phase 4 — Integration Layer (Filter + Prompt)

**Goal:** Deterministically reduce the dataset to a candidate set and build a strong LLM prompt.

### Tasks
1. **Filter engine (`src/integration/filter.py`)**
   - Location filter (case-insensitive contains/exact)
   - Cuisine filter (token/substring against cuisine list)
   - `rating >= min_rating`
   - `budget_band == requested budget` (or cost within mapped thresholds)
   - Sort by rating (and votes if available)
   - Truncate to `max_candidates` (e.g. 20–50)
2. **Serializer (`src/integration/serializer.py`)**
   - Convert candidates to compact dict/JSON:
     - name, location, cuisine, rating, cost, budget_band, optional extras
   - Keep token footprint small
3. **Prompt builder (`src/integration/prompt_builder.py`)**
   - System role: Zomato-like recommendation expert
   - Include user preferences block
   - Include candidate list
   - Instructions:
     - rank by fit
     - explain each pick
     - use only provided candidates
     - return strict JSON matching schema
   - Optional summary instruction
4. Empty-set path:
   - If zero candidates, skip LLM and return structured “no match” result with relaxation hints

### Deliverables
- [ ] Deterministic filter function with metrics (counts per stage)
- [ ] Prompt templates (system + user)
- [ ] Candidate JSON serializer
- [ ] Tests with fixture DataFrame slices

### Exit criteria
For sample preferences, system returns a non-empty candidate list (when data allows) and a fully rendered prompt string/messages array.

### Suggested filter metrics to log
- rows_total → after_location → after_cuisine → after_rating → after_budget → after_truncate

---

## Phase 5 — LLM Recommendation Engine

**Goal:** Turn candidates + preferences into ranked, explained recommendations.

### Tasks
1. **LLM client (`src/recommendation/llm_client.py`)**
   - Wrap provider SDK
   - Config-driven model, temperature, timeout
   - Centralized API key loading
2. **Output parser (`src/recommendation/parser.py`)**
   - Parse JSON from model response
   - Repair path: strip markdown fences; optional one retry with “fix JSON” prompt
   - Validate schema (rank, restaurant_name, cuisine, rating, estimated_cost, explanation)
3. **Engine (`src/recommendation/engine.py`)**
   - Orchestrate: preferences + candidates → prompt → LLM → parse → guardrails
   - Guardrail: keep only restaurants whose names exist in candidate set
   - Sort by returned rank; slice to `top_n`
4. **Prompt tuning**
   - Add explicit tie-breakers: rating, budget fit, cuisine specificity, additional preferences
   - Ask for concise explanations (1–2 sentences)
5. **Fallback behavior**
   - On LLM failure: optional deterministic fallback (top rated candidates + template explanations) OR clean error

### Deliverables
- [ ] Working `recommend(preferences, candidates) -> RecommendationResult`
- [ ] JSON schema + parser tests (including messy outputs)
- [ ] Hallucination filter
- [ ] Example successful end-to-end call on real subset

### Exit criteria
Given a known candidate set, engine returns Top-N recommendations with usable explanations and no invented restaurants.

---

## Phase 6 — API & Frontend Layer

**Goal:** Build a robust FastAPI backend and a high-quality, polished Next.js frontend named `stitch_tablemate_ai_recommendation_engine`.

### Tasks
1. **API Development (FastAPI)**
   - Create `src/api/main.py`
   - `POST /api/v1/recommendations`
   - Request/response models aligned with architecture
   - Proper HTTP error mapping (400/404/502)
   - Configure CORS for frontend access
2. **Frontend Setup (`stitch_tablemate_ai_recommendation_engine`)**
   - Initialize Next.js project (React, TypeScript, Tailwind CSS)
   - Implement premium, responsive UI design with modern aesthetics (glassmorphism, smooth animations)
   - Form inputs for all preference fields (location, budget, cuisine, etc.)
   - Results panel with interactive cards displaying Restaurant Name, Cuisine, Rating, Estimated Cost, and AI Explanation
3. **Integration & Polish**
   - Connect frontend to FastAPI backend
   - Handle loading states, empty results, and errors gracefully

### Deliverables
- [ ] FastAPI endpoint working and tested
- [ ] High-quality Next.js frontend (`stitch_tablemate_ai_recommendation_engine`)
- [ ] Seamless integration between UI and backend

### Exit criteria
A non-technical user can open the Next.js UI in their browser, enter preferences, and view the AI-generated recommendations in a beautifully designed, responsive interface.

---

## Phase 7 — Reliability, Guardrails & Testing

**Goal:** Make the system robust enough for demos and repeated use.

### Tasks
1. **Edge cases**
   - No candidates
   - Missing optional columns
   - All LLM recommendations hallucinated → empty after guardrail
   - Very large city subset (performance)
2. **Observability**
   - Log filter funnel counts
   - Log latency for LLM calls
   - Log parse retries/failures (no secrets)
3. **Tests**
   - Unit: preprocess, budget banding, filters, parser, guardrails
   - Integration: mocked LLM end-to-end
   - Golden prompt fixtures (optional)
4. **Config hardening**
   - Timeouts, max tokens, max candidates
   - Safe defaults for demos
5. **Security hygiene**
   - `.env` not committed
   - Sanitize free-text additional preferences in prompts

### Deliverables
- [ ] `tests/` with meaningful coverage of core logic
- [ ] Mocked LLM tests (no network required in CI)
- [ ] Failure-path demos documented

### Exit criteria
Core pipeline is testable offline; production-ish failure modes degrade gracefully.

---

## Phase 8 — Polish, Documentation & Release

**Goal:** Package a clear demo-ready project.

### Tasks
1. Write `README.md`:
   - Problem overview
   - Setup (venv, deps, `.env`)
   - Dataset note + first-run cache behavior
   - How to run CLI / UI / API
   - Example input/output
2. Add sample queries (Delhi + Chinese, Bangalore + Italian, etc.).
3. Add architecture/implementation doc links.
4. Record known limitations (static dataset, no live booking, possible city coverage gaps).
5. Final demo script / screenshot section (if UI).
6. Tag version `v0.1.0`.

### Deliverables
- [ ] Complete README
- [ ] `.env.example` finalized
- [ ] Demo script or make targets (`make run`, `make test`)
- [ ] Short changelog

### Exit criteria
New contributor can set up and run a full recommendation in under 15 minutes.

---

## Cross-Phase Technical Checklist

### Data fields (minimum)
- [ ] restaurant_name
- [ ] location/city
- [ ] cuisine
- [ ] cost → budget band
- [ ] rating

### User preferences (minimum)
- [ ] location
- [ ] budget (low/medium/high)
- [ ] cuisine
- [ ] minimum rating
- [ ] additional preferences (optional)

### LLM output (minimum)
- [ ] ranked list
- [ ] explanation per item
- [ ] optional summary
- [ ] structured/parseable format

### Architecture alignment
- [ ] Data Layer
- [ ] Input Layer
- [ ] Integration Layer (filter + prompt)
- [ ] Recommendation Engine
- [ ] Presentation Layer

---

## Suggested Timeline (indicative)

| Phase | Indicative effort |
|-------|-------------------|
| 1 Foundation | 0.5 day |
| 2 Data | 1 day |
| 3 Input | 0.5 day |
| 4 Integration | 1 day |
| 5 LLM engine | 1–1.5 days |
| 6 Presentation | 0.5–1 day |
| 7 Testing & hardening | 1 day |
| 8 Polish & docs | 0.5 day |
| **Total** | **~6–7 days** for a solid MVP |

(Adjust based on UI/API scope and LLM provider complexity.)

---

## MVP vs Later Enhancements

### MVP (must ship)
- HF dataset load + cache
- Preference validation
- Deterministic filters
- LLM rank + explanations
- FastAPI endpoint
- High-quality Next.js frontend (`stitch_tablemate_ai_recommendation_engine`)
- Basic guardrails + README

### Post-MVP (nice to have)
- Fuzzy location matching
- Embeddings / semantic retrieval
- Multi-turn refinement chat
- Per-city budget calibration UI
- Dockerization and cloud deploy
- User history / personalization

---

## Implementation Order Inside Each Coding Session

1. Write/adjust data structures and interfaces first  
2. Implement deterministic logic (preprocess/filter) with tests  
3. Add LLM orchestration behind a narrow interface  
4. Wire presentation  
5. Only then refine prompt quality using real examples  

---

## Risk Register

| Risk | Impact | Plan |
|------|--------|------|
| Dataset schema differs from assumptions | High | Schema probe notebook + flexible mapper early in Phase 2 |
| LLM output format drift | High | Strict schema + retry + deterministic fallback |
| Token overflow from too many candidates | Medium | Hard cap + compact serializer |
| City/cuisine coverage sparse | Medium | Empty-state guidance; loosen match rules optionally |
| API cost during dev | Medium | Cache candidates; use smaller model for dev |
| Over-filtering → zero results | Medium | Log funnel; suggest which constraint to relax |

---

## Phase Dependency Graph

```text
Phase 1 Foundation
    │
    ▼
Phase 2 Data Ingestion ──────────────┐
    │                                │
    ▼                                │
Phase 3 User Input                   │
    │                                │
    ├───────────────┐                │
    ▼               ▼                │
Phase 4 Filters   Prompt Builder ◄───┘
    │               │
    └───────┬───────┘
            ▼
    Phase 5 LLM Engine
            │
            ▼
    Phase 6 Presentation
            │
            ▼
    Phase 7 Hardening & Tests
            │
            ▼
    Phase 8 Docs & Release
```

---

## First Concrete Build Slice (start here)

After Phase 1 setup, implement this thin vertical slice ASAP:

1. Load a sample of the dataset  
2. Hardcode one `UserPreferences` object  
3. Filter candidates  
4. Call LLM with prompt  
5. Print top 3 recommendations  

This validates the full architecture early before investing in UI polish.

---

## Success Metrics (plan tracking)

| Metric | Target |
|--------|--------|
| End-to-end happy path | Works for ≥3 sample preference sets |
| Hard-constraint fidelity | 100% of final recs pass location/cuisine/budget/rating filters |
| Hallucinated restaurants | 0 after guardrails |
| Time to first successful demo | Within Phases 1–5 |
| Offline testability | Filter/preprocess/parser tests run without LLM key |

---

