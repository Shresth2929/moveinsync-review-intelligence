from src.classify_reviews import classify_text, classify_df, OTHER, validation_error_rate
from src.clean_reviews import clean_reviews


def test_crash_and_login_multilabel():
    r = classify_text("app crashes on login every time", 1)
    assert "Crashes, freezing and app stability" in r["categories"]
    assert "Login, authentication and account access" in r["categories"]
    assert r["evidence"]


def test_positive_high_star():
    assert classify_text("Great app, easy to use", 5)["categories"] == ["Positive feedback"]


def test_negated_positive_not_positive():
    assert "Positive feedback" not in classify_text("not good at all", 1)["categories"]


def test_no_match_flags_manual_review_for_negative():
    r = classify_text("xyzzy", 1)
    assert r["categories"] == [OTHER] and r["needs_manual_review"]


def test_missing_text():
    assert classify_text(None, 1)["categories"] == [OTHER]


def test_classify_df_columns(synthetic):
    df, _ = clean_reviews(synthetic)
    out = classify_df(df)
    assert {"categories", "evidence", "confidence", "needs_manual_review"} <= set(out.columns)


def test_validation_without_labels(tmp_path):
    p = tmp_path / "v.csv"
    p.write_text("review_id,rating,text,categories,manual_categories\n1,1,x,Other,\n")
    assert validation_error_rate(str(p))["labeled"] == 0
