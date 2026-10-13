import pandas as pd
from src.clean_reviews import clean_reviews, merge_with_existing


def test_invalid_rating_dropped_and_duplicates_removed(synthetic):
    df, s = clean_reviews(synthetic)
    assert s["dropped_invalid_rating"] == 1
    assert s["dropped_duplicates"] == 1
    assert df["rating"].between(1, 5).all()
    assert df["review_id"].is_unique


def test_empty_row_dropped_missing_counts(synthetic):
    df, s = clean_reviews(synthetic)
    assert s["dropped_empty_row"] == 1  # empty text AND no date
    assert s["missing_version"] == len(df)  # optional column absent


def test_empty_dataset():
    df, s = clean_reviews(pd.DataFrame())
    assert len(df) == 0 and s["output_rows"] == 0


def test_missing_id_gets_hash_key():
    raw = pd.DataFrame({"score": [3], "content": ["hello world"], "at": ["2025-01-01"]})
    df, _ = clean_reviews(raw)
    assert df["review_id"].iloc[0].startswith("h_")


def test_merge_idempotent(synthetic):
    df, _ = clean_reviews(synthetic)
    once = merge_with_existing(df, df)
    assert len(once) == len(df)


def test_csv_export_roundtrip(synthetic, tmp_path):
    df, _ = clean_reviews(synthetic)
    p = tmp_path / "x.csv"
    df.to_csv(p, index=False)
    assert len(pd.read_csv(p)) == len(df)
