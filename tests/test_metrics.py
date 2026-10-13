import pandas as pd
from src import analyze_reviews as A
from src.classify_reviews import classify_df
from src.clean_reviews import clean_reviews


def _df(synthetic):
    c, _ = clean_reviews(synthetic)
    return classify_df(c)


def test_overview_denominators(synthetic):
    ov = A.overview(_df(synthetic))
    assert ov["n_reviews"] == 4 and ov["negative_count"] == 2
    assert ov["negative_pct"] == 50.0 and ov["negative_denominator"] == 4


def test_issue_table_uses_negative_denominator(synthetic):
    it = A.issue_table(_df(synthetic))
    assert (it["denominator"] == 2).all()
    assert it["pct_of_denominator"].max() <= 100


def test_multilabel_can_exceed_100():
    d = pd.DataFrame({"review_id": ["1"], "rating": [1], "categories": ["A|B"], "confidence": ["medium"]})
    it = A.issue_table(d)
    assert it["pct_of_denominator"].sum() == 200.0


def test_empty_dataset_functions():
    e = pd.DataFrame(columns=["review_id", "rating", "text", "review_date", "categories", "app_version", "has_developer_reply", "confidence"])
    assert A.overview(e)["n_reviews"] == 0
    assert A.issue_table(e).empty
    assert A.monthly_trend(e).empty
    assert A.period_comparison(e)["available"] is False


def test_rating_distribution_sums(synthetic):
    d = A.rating_distribution(_df(synthetic))
    assert d["count"].sum() == 4


def test_period_comparison_insufficient_and_flag():
    rows = []
    for i in range(40):  # SYNTHETIC: previous period low negatives, current high
        rows.append({"review_id": f"p{i}", "rating": 5 if i % 10 else 1, "review_date": pd.Timestamp("2025-01-01") + pd.Timedelta(days=i % 25), "categories": "Other or insufficient evidence", "confidence": "low"})
    for i in range(40):
        rows.append({"review_id": f"c{i}", "rating": 1 if i % 10 else 5, "review_date": pd.Timestamp("2025-02-05") + pd.Timedelta(days=i % 25), "categories": "Booking and cancellation", "confidence": "medium"})
    r = A.period_comparison(pd.DataFrame(rows), days=30)
    assert r["available"] and r["flags"]
    r2 = A.period_comparison(pd.DataFrame(rows[:5]), days=30)
    assert r2["available"] is False


def test_reply_coverage_unobservable(synthetic):
    assert A.reply_coverage(_df(synthetic))["observable"] is False
