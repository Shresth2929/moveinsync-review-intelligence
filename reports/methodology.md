# Methodology, assumptions, limitations and tools

## Pipeline
`collect/import → clean → merge (idempotent on review_id) → classify → metrics → period comparison/flags → report`.
Run with `python -m src.pipeline`. Re-running never duplicates rows; if collection fails, existing data is preserved and the error is stored in `data/collection_meta.json`.

## Data collection
- Target: `com.moveinsync.ets`, country `in`, language `en`, sort `NEWEST` (configurable via env vars in `.env.example`).
- Method: `google-play-scraper`, an **unofficial** community library (not an official Google API; may break, may be subject to Google Play ToS). Authorized alternatives: Play Developer API / Play Console export, supported via CSV import.
- **Status in this submission environment:** the build sandbox could not resolve `play.google.com` (`Name or service not known`), so **no reviews were collected here and no findings are reported.** `reports/executive_recommendations.md` states this explicitly and is regenerated with real numbers once data is loaded.

## Metrics definitions
- Negative review = 1-2★. Star rating is not sentiment; it is only used as a bucket.
- Issue share = reviews in negative set mentioning the theme / all negative reviews (denominator shown everywhere). Multi-label, so shares may sum above 100%.
- Displayed Play rating (all ratings) ≠ sample mean (written reviews only).
- Period comparison: latest N days vs previous N days, anchored on newest review date; needs ≥20 reviews per period (configurable).
- Priority score = frequency % × severity × keyword confidence ÷ effort. Severity (1-5) and effort (S/M/L) are **analyst estimates** in `src/analyze_reviews.py`, not observed values.

## Classification
Transparent regex rules in `src/classify_reviews.py` (15 categories, multi-label), each with matched evidence. Categories are hypotheses. `owner_type` separates app-fixable (`app`), operations/support (`ops`) and `mixed`. Negative reviews with no match are flagged `needs_manual_review`.

## Validation procedure (to be performed once real data exists)
1. `python -m src.pipeline --validation-sample` writes 50 random reviews to `data/validation_sample.csv`.
2. A human fills `manual_categories` (pipe-separated, same category names).
3. `python -c "from src.classify_reviews import validation_error_rate as v; print(v('data/validation_sample.csv'))"` reports exact-match error rate and no-overlap rate.
Observed error rate: **not yet measured (no real data was available)**. No accuracy figure is claimed.

## Limitations
Self-selected written reviews; keyword rules miss sarcasm, Hinglish/transliterated text and context; no causal claims about releases; reply coverage only if reply fields are present; crash, funnel, ETA and notification metrics need internal MoveInSync data.

## Tools
Python 3, pandas, Streamlit, Plotly, pytest, GitHub Actions. No LLM used; none is needed for the rule-based baseline.
