# MoveInSync Review Intelligence

Reproducible review-analysis and decision-support system for the MoveInSync app (`com.moveinsync.ets`) Google Play ratings.

> **Honest status:** the environment this was built in could not reach Google Play, so **no real reviews have been collected yet** and the executive report contains no findings. The pipeline, dashboard, tests and CSV-import path are complete and tested (with clearly labeled synthetic fixtures used only inside `tests/`). Load real data with one of the commands below to generate the real report.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # optional; no secrets needed
```

## Run
```bash
# 1) Real data, option A: collect (unofficial scraper; needs internet)
python -m src.pipeline --collect

# 1) Real data, option B: import a CSV (Play Console export or other permitted source)
python -m src.pipeline --import-csv path/to/reviews.csv --displayed-rating <value shown on the Play listing>

# 2) Manual validation sample (then fill manual_categories and score it, see reports/methodology.md)
python -m src.pipeline --validation-sample

# 3) Dashboard
streamlit run app.py

# 4) Tests
python -m pytest -q
```
Outputs: `data/reviews_clean.csv`, `data/reviews_categorized.csv`, `data/collection_meta.json`, `data/latest_flags.json`, `reports/executive_recommendations.md`.

## Structure
`app.py` dashboard · `src/` collect, clean, classify, analyze, report, pipeline · `tests/` 22 tests · `reports/methodology.md` · `.github/workflows/weekly_analysis.yml` weekly scheduled run (collection may fail on CI; data is then preserved).

## Notes
- The scraper is unofficial and not a Google API; see `reports/methodology.md`.
- Never mix synthetic fixtures with real data.
