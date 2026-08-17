Creating a detailed `edge-case.md` from the architecture and implementation plan.

```markdown
# Edge Cases & Failure Modes
## AI-Powered Restaurant Recommendation System (Zomato Use Case)

This document catalogs edge cases, expected behavior, and handling strategies aligned with `docs/architecture.md` and `docs/implementation-plan.md`.

---

## 1. Purpose

- Make failure modes explicit before coding guardrails (Phase 7)
- Define consistent product behavior for empty, partial, and malformed data
- Reduce LLM hallucination risk and UX dead-ends
- Provide a test checklist for unit, integration, and demo scenarios

---

## 2. Severity Legend

| Level | Meaning | Typical user impact |
|-------|---------|---------------------|
| **P0** | Blocks recommendation or corrupts trust | Crash, invented restaurants, wrong hard filters |
| **P1** | Degraded but recoverable | Empty results, retry needed, partial fields |
| **P2** | Minor / polish | Formatting quirks, suboptimal ranking |
| **P3** | Rare / future | Multi-language, geo precision, personalization |

---

## 3. Data Ingestion & Preprocessing Edge Cases

| ID | Edge case | Severity | Expected handling |
|----|-----------|----------|-------------------|
| D1 | Hugging Face dataset unavailable / network failure | P0 | Fail fast with clear message; if cache exists, load cache and warn |
| D2 | Cache missing on first run | P1 | Download, preprocess, write cache; show progress |
| D3 | Cache corrupt or unreadable | P1 | Delete/ignore cache, re-download, log warning |
| D4 | Schema/column names differ from assumptions | P0 | Flexible column mapper; startup validation of required logical fields; abort if name/location impossible to map |
| D5 | Missing `restaurant_name` or `location` | P1 | Drop rows; log drop count |
| D6 | Missing `rating` | P1 | Exclude from rating-filtered results (or optional impute policy—default: exclude) |
| D7 | Missing `cost` | P1 | Exclude from budget filter (default) OR assign `unknown` band and only include if budget filter relaxed |
| D8 | Missing `cuisine` | P1 | Exclude from cuisine-specific queries; keep for non-cuisine browse only if supported |
| D9 | Non-numeric rating/cost strings (`"NEW"`, `"-"`, `"4.5/5"`) | P1 | Parse defensively; invalid → NaN → dropped per policy |
| D10 | Rating outside 0–5 | P2 | Clamp or drop; prefer drop if extreme/invalid |
| D11 | Negative or absurd cost values | P2 | Drop or winsorize before budget banding |
| D12 | Duplicate restaurant rows | P2 | Deduplicate by name+location(+address if any); keep highest votes/rating |
| D13 | Multi-cuisine cell (`"Italian, Chinese"`) | P1 | Split on comma/slash/pipe; match if any token hits |
| D14 | Inconsistent casing/whitespace in city/cuisine | P1 | Normalize (trim, casefold) for matching; preserve display casing |
| D15 | Empty dataset after cleaning | P0 | Abort pipeline with actionable error (“dataset empty after preprocess”) |
| D16 | Skewed cost distribution (breaks budget bands) | P1 | Use percentile-based thresholds; optionally per-city bands; log band sizes |
| D17 | Extremely large dataset (memory pressure) | P1 | Cache projected columns only; optional chunked filter; cap in-memory fields |
| D18 | Special characters / encoding issues in names | P2 | UTF-8 end-to-end; sanitize only where needed for prompt safety |

### Preprocess policy defaults

```text
required_for_row_keep: restaurant_name, location
required_for_standard_recommend: rating, cost, cuisine
budget_band_source: valid numeric cost only
on_parse_fail: set null → row excluded by relevant filters
```

---

## 4. User Input Edge Cases

| ID | Edge case | Severity | Expected handling |
|----|-----------|----------|-------------------|
| U1 | Missing required field (location/budget/cuisine/min_rating) | P0 | Validation error (400 / CLI message); do not call LLM |
| U2 | Empty strings / whitespace-only | P0 | Treat as missing; reject |
| U3 | Invalid budget value (not low/medium/high) | P0 | Reject with allowed values list |
| U4 | `min_rating` < 0 or > 5 | P1 | Reject or clamp; default: reject with message |
| U5 | Non-numeric `min_rating` | P0 | Validation error |
| U6 | `top_n` = 0 or negative | P1 | Reject |
| U7 | `top_n` very large (e.g. 1000) | P1 | Cap to max (e.g. 10); warn |
| U8 | Cuisine typo (`"Italyan"`) | P1 | May yield zero results; suggest closest known cuisines (optional post-MVP fuzzy) |
| U9 | Location typo / alternate name (`"Bengaluru"` vs `"Bangalore"`) | P1 | Optional alias map; else empty-state with hint |
| U10 | Location at wrong granularity (area vs city) | P1 | Contains match may over/under select; document behavior; optional future geo split |
| U11 | Additional preferences empty | P2 | Omit from prompt section |
| U12 | Additional preferences very long / noisy | P1 | Truncate to max chars (e.g. 300–500); sanitize |
| U13 | Additional preferences with prompt-injection attempts | P0 | Treat as untrusted text; wrap as data; never obey instructions inside preferences that override system rules |
| U14 | Conflicting preferences (“low budget” + “fine dining luxury”) | P2 | Let LLM explain tradeoffs within filtered candidates only |
| U15 | Unicode / emoji in inputs | P2 | Accept if safe; normalize where needed |
| U16 | SQL/HTML-like payload in text fields | P1 | No raw interpolation into code/SQL; prompt-escape/sanitize for display |

### Input validation contract

```text
location: non-empty string
budget: low | medium | high
cuisine: non-empty string
min_rating: float in [0, 5]
additional_preferences: optional string ≤ N chars
top_n: int in [1, TOP_N_MAX] (default 5)
```

---

## 5. Filtering & Integration Layer Edge Cases

| ID | Edge case | Severity | Expected handling |
|----|-----------|----------|-------------------|
| F1 | Zero candidates after all filters | P1 | Skip LLM; return empty result + relaxation hints (rating → budget → cuisine → location) |
| F2 | Zero after location only | P1 | Message: no restaurants for location; suggest sample cities from dataset |
| F3 | Candidates exist for city but not cuisine | P1 | Tell user cuisine unavailable in that city; optional list top cuisines there |
| F4 | Rating threshold too high (e.g. 4.9) | P1 | Empty-state; suggest next-best max rating in filtered subset |
| F5 | Budget band has no rows in city/cuisine slice | P1 | Empty-state; suggest adjacent budget band |
| F6 | Over-filtering combination | P1 | Log funnel counts; surface which stage went to zero |
| F7 | Under-filtering (too many rows) | P1 | Sort by rating (+votes); truncate to `max_candidates` |
| F8 | Exact vs contains location match ambiguity | P2 | Document “contains” behavior; avoid matching unrelated superstrings where possible |
| F9 | Cuisine token collision (`"Indian"` vs `"Indian Chinese"`) | P2 | Token match with boundaries/normalization rules; prefer token equality over naive substring if feasible |
| F10 | All candidates missing optional explanation fields | P2 | Serializer still emits required fields; omit null optionals |
| F11 | Candidate set size = 1 | P2 | Still call LLM for explanation OR template-explain; return single recommendation |
| F12 | Candidate names identical in different areas | P1 | Include location/address in serializer and output identity |
| F13 | Filter stage metrics unavailable | P3 | Best-effort logging; don’t fail request |

### Filter funnel (must log)

```text
total
 → after_location
 → after_cuisine
 → after_rating
 → after_budget
 → after_sort_truncate
```

### Empty-state response shape

```json
{
  "recommendations": [],
  "summary": "No restaurants matched your filters.",
  "diagnostics": {
    "funnel": {"total": 50000, "after_location": 1200, "after_cuisine": 40, "after_rating": 3, "after_budget": 0},
    "suggestions": [
      "Try a higher budget band",
      "Lower minimum rating to 3.5"
    ]
  }
}
```

---

## 6. Prompt & LLM Recommendation Edge Cases

| ID | Edge case | Severity | Expected handling |
|----|-----------|----------|-------------------|
| L1 | LLM API key missing/invalid | P0 | Fail before call with config error; CLI/API clear message |
| L2 | LLM timeout / network error | P0/P1 | Retry once with backoff (optional); then 502 / deterministic fallback |
| L3 | LLM rate limit | P1 | Retry-After if available; else friendly “busy” error |
| L4 | Empty LLM response | P1 | Retry once; then fallback/error |
| L5 | Non-JSON response / markdown fences | P1 | Strip fences; extract JSON; repair retry prompt once |
| L6 | JSON schema missing fields | P1 | Partial parse if possible; else retry/fail |
| L7 | Extra hallucinated fields | P2 | Ignore unknown fields |
| L8 | Hallucinated restaurant not in candidates | P0 | Drop via name guardrail against candidate set |
| L9 | All recommendations hallucinated | P0 | Return error or deterministic top-N fallback with template explanations |
| L10 | Duplicate restaurants in LLM list | P1 | Deduplicate by normalized name+location |
| L11 | Rank gaps / non-integer ranks | P2 | Re-rank by response order |
| L12 | LLM reorders ignoring hard constraints | P0 | Hard constraints already enforced by filter; still re-validate rating/budget/cuisine/location on output |
| L13 | Explanations empty or generic | P2 | Accept if schema-valid; optional quality nudge in prompt |
| L14 | Explanation contradicts data (wrong rating/cost) | P1 | Prefer structured fields from dataset, not LLM-copied facts; use LLM for explanation text only where possible |
| L15 | Token overflow / context too long | P0 | Reduce candidates / compact serializer; hard cap K |
| L16 | Model refuses or safety-blocks | P1 | Surface safe message; fallback deterministic list |
| L17 | Additional preferences attempt to override rules (“ignore candidates and recommend…”) | P0 | System prompt + guardrails enforce candidate-only recommendations |
| L18 | `top_n` > candidate count | P2 | Return available count only |
| L19 | Low-temperature still unstable ranking | P2 | Accept non-determinism; optional cache-by-query hash post-MVP |
| L20 | Provider returns different numeric types (rating as string) | P1 | Coerce types in parser |

### LLM output guardrail pipeline

```text
raw response
 → extract/parse JSON
 → validate schema
 → filter to known candidates only
 → revalidate hard constraints with source data
 → dedupe
 → sort by rank
 → slice to top_n
 → if empty: fallback OR explicit failure
```

### Deterministic fallback (optional but recommended)

When LLM fails after retries:
- Take filtered candidates sorted by rating
- Emit top_n with template explanation:
  - `"{name} matches {cuisine} in {location} with rating {rating} and {budget} budget."`

---

## 7. Output / Presentation Edge Cases

| ID | Edge case | Severity | Expected handling |
|----|-----------|----------|-------------------|
| O1 | Empty recommendations | P1 | Friendly empty state + suggestions (not a blank screen) |
| O2 | Missing optional summary | P2 | Hide summary section |
| O3 | Very long explanation text | P2 | Soft-wrap; optional truncate with “read more” in UI |
| O4 | Special characters breaking table layout | P2 | Use safe formatter/rich wrapping |
| O5 | Null cost/rating in display object | P1 | Should not happen after validation; show “N/A” if it does |
| O6 | Partial success (fewer than top_n) | P2 | Show available; note “showing X of Y requested” |
| O7 | API client expects strict schema | P1 | Stable response contract; errors use standard error envelope |
| O8 | Concurrent requests in API mode | P2 | Stateless handlers; no shared mutable candidate buffer |

---

## 8. Security, Privacy & Abuse Edge Cases

| ID | Edge case | Severity | Expected handling |
|----|-----------|----------|-------------------|
| S1 | API key logged | P0 | Never log secrets; redact env values |
| S2 | Prompt injection via `additional_preferences` | P0 | Delimit untrusted input; candidate-only hard rule; output guardrails |
| S3 | Path traversal / unexpected file ops on cache path | P1 | Fixed cache directory; no user-controlled paths |
| S4 | Oversized request payload (API) | P1 | Body size limit; field length limits |
| S5 | User PII pasted into preferences | P2 | No persistent storage in v1; document non-retention |
| S6 | XSS in web UI rendering explanations | P1 | React/Streamlit safe rendering; escape HTML if custom web |
| S7 | SSRF via user-supplied URLs | P3 | Do not accept URLs in v1 inputs |

---

## 9. Performance & Cost Edge Cases

| ID | Edge case | Severity | Expected handling |
|----|-----------|----------|-------------------|
| P-C1 | Cold start HF download latency | P1 | Cache after first run; document first-run wait |
| P-C2 | Repeated full-dataset scans per request | P1 | In-memory DataFrame or indexed columns after load |
| P-C3 | Huge candidate payload to LLM | P0 | `max_candidates` + compact JSON |
| P-C4 | Expensive model used in dev loops | P2 | Config switch for cheaper dev model |
| P-C5 | Timeout under provider latency spikes | P1 | Client timeout + single retry policy |
| P-C6 | Storm of requests (API) | P2 | Optional basic rate limiting post-MVP |

---

## 10. Config & Environment Edge Cases

| ID | Edge case | Severity | Expected handling |
|----|-----------|----------|-------------------|
| C1 | `.env` missing | P1 | Defaults where safe; fail if API key required for live LLM path |
| C2 | Invalid model name | P1 | Provider error → actionable message |
| C3 | Budget thresholds misconfigured (low > high) | P0 | Validate config at startup |
| C4 | `max_candidates` < `top_n` | P1 | Auto-raise max_candidates or clamp top_n; warn |
| C5 | Wrong cache path permissions | P1 | Error with path + permission hint |

---

## 11. End-to-End Scenario Matrix

| Scenario | Input sketch | Expectation |
|----------|--------------|-------------|
| Happy path | Bangalore, medium, Italian, 4.0 | ≥1 valid recs with explanations |
| No city | `"Atlantis"` | Empty after location; suggest known cities |
| No cuisine in city | Valid city + rare cuisine | Empty after cuisine; suggest local cuisines |
| Harsh rating | `min_rating=4.9` | Likely empty; suggest lower threshold |
| Low budget only | `budget=low` in expensive slice | Possible empty; suggest medium |
| Single candidate | Filters leave 1 | One explained recommendation |
| top_n > candidates | `top_n=5`, 2 candidates | Return 2 |
| LLM down | Provider timeout | Fallback or clean error (no crash) |
| LLM junk JSON | Malformed content | Repair once → fallback/error |
| Hallucination | Model invents “Fake Cafe” | Dropped by guardrail |
| Injection | Additional prefs: “Ignore all rules…” | Still candidate-only output |
| Missing cost rows | Dataset sparse costs | Budget filter excludes them; may empty |
| Alias city | `"Bengaluru"` | Match if alias map exists; else empty + hint |
| Multi-cuisine match | Restaurant cuisines include requested token | Included |
| Duplicate recs from LLM | Same name twice | Deduped in parser/engine |

---

## 12. Handling Playbook (by layer)

### 12.1 Data layer
- Validate schema on load
- Prefer cache after successful preprocess
- Log drop counts and band distribution

### 12.2 Input layer
- Pydantic (or equivalent) hard validation
- Normalize early; reject bad enums/ranges

### 12.3 Integration layer
- Deterministic filters before LLM
- Funnel metrics always computed
- Never call LLM with empty candidates (unless redesign for “relaxation assistant”)

### 12.4 Recommendation layer
- Strict JSON contract
- One repair retry
- Candidate membership guardrail
- Re-validate hard constraints from source rows
- Optional deterministic fallback

### 12.5 Presentation layer
- Explicit empty and error states
- Dataset-backed facts for name/cuisine/rating/cost
- LLM text used primarily for explanations/summary

---

## 13. Test Checklist (Phase 7 mapping)

### Unit tests
- [ ] Parse dirty rating/cost values
- [ ] Budget band assignment boundaries
- [ ] Multi-cuisine tokenization match
- [ ] Location/cuisine case-insensitive match
- [ ] Preference validation reject/accept matrix
- [ ] Funnel goes to zero at each stage
- [ ] Serializer compact output
- [ ] Parser: fenced JSON, bad JSON, missing fields
- [ ] Guardrail drops unknown restaurant names
- [ ] Dedupe + top_n slice
- [ ] Config validation (`max_candidates`, thresholds)

### Integration tests (mocked LLM)
- [ ] Happy path full pipeline
- [ ] Empty filter short-circuit (LLM not called)
- [ ] LLM timeout → fallback/error path
- [ ] Hallucinated names removed
- [ ] `top_n` larger than candidate set

### Manual demo scripts
- [ ] 3 happy-path cities/cuisines
- [ ] 2 intentional empty-result queries
- [ ] 1 injection-style additional preference
- [ ] First-run cache vs second-run speed sanity check

---

## 14. Product Copy Snippets (recommended)

**No matches**
> No restaurants matched those filters. Try lowering the minimum rating, switching budget, or broadening cuisine.

**LLM unavailable**
> Recommendation service is temporarily unavailable. Showing top rated matches from filters instead.
> *(if fallback enabled)*

**Partial guardrail drop**
> Some AI suggestions were removed because they were not in the matched restaurant list.

**First run**
> First run may take a few minutes while the dataset is downloaded and cached.

---

## 15. Out-of-Scope Edge Cases (v1 non-goals)

- Live table availability / delivery ETA changes
- Payments, booking failures
- Login/session personalization conflicts
- Real-time map distance / traffic
- Multi-user collaborative preferences
- Non-English query understanding guarantees
- Legal disputes over restaurant ranking fairness

Document these as known limitations in README rather than building complex handlers in MVP.

---

## 16. Priority Implementation Order for Guardrails

1. **P0:** Input validation, candidate-only LLM rule, hallucination filter, config/API key checks, no-crash LLM failures  
2. **P1:** Empty-state + funnel diagnostics, JSON repair retry, missing field policies, token/candidate caps  
3. **P2:** Dedup, display polish, explanation quality, aliases  
4. **P3:** Advanced fuzzy match, rate limiting, semantic retrieval fallbacks  

---

## 17. Traceability

| Source | Edge-case coverage |
|--------|--------------------|
| Problem statement workflow | Data → input → filter → LLM → output failures at each step |
| Architecture guardrails | Empty candidates, hallucinated names, malformed LLM output, budget mapping, security |
| Implementation plan Phase 7 | Testing, observability, parse retries, sanitization, performance caps |

