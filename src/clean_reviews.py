"""Normalize, validate and deduplicate review records. Original text is preserved."""
from __future__ import annotations
import hashlib
import pandas as pd

CANONICAL = ["review_id", "rating", "text", "review_date", "collected_at",
             "app_version", "has_developer_reply", "language", "source", "thumbs_up"]

ALIASES = {
    "reviewid": "review_id", "id": "review_id", "review id": "review_id",
    "score": "rating", "stars": "rating", "star_rating": "rating", "star rating": "rating",
    "content": "text", "review": "text", "review_text": "text", "review text": "text", "body": "text",
    "at": "review_date", "date": "review_date", "review date": "review_date", "review_submit_date": "review_date",
    "reviewcreatedversion": "app_version", "appversion": "app_version", "version": "app_version",
    "review_submit_version": "app_version", "app version": "app_version",
    "replycontent": "reply_text", "developer reply text": "reply_text", "developer_reply": "reply_text",
    "thumbsupcount": "thumbs_up", "thumbs up": "thumbs_up", "thumbs_up_count": "thumbs_up",
}


def _norm_cols(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [ALIASES.get(str(c).strip().lower(), str(c).strip().lower()) for c in df.columns]
    return df.loc[:, ~df.columns.duplicated()]


def _make_key(row) -> str:
    raw = f"{row.get('text','')}|{row.get('review_date','')}|{row.get('rating','')}"
    return "h_" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def clean_reviews(raw: pd.DataFrame, source: str = "unknown", collected_at: str | None = None):
    """Return (clean_df, stats). Invalid ratings (not integer 1-5) and fully empty rows are dropped."""
    stats = {"input_rows": int(len(raw)), "dropped_invalid_rating": 0, "dropped_empty_row": 0,
             "dropped_duplicates": 0, "missing_text": 0, "missing_date": 0, "missing_version": 0}
    if raw is None or len(raw) == 0:
        stats["output_rows"] = 0
        return pd.DataFrame(columns=CANONICAL), stats
    df = _norm_cols(raw)
    for c in CANONICAL:
        if c not in df.columns:
            df[c] = pd.NA
    if "reply_text" in df.columns and df["has_developer_reply"].isna().all():
        df["has_developer_reply"] = df["reply_text"].notna() & (df["reply_text"].astype(str).str.strip() != "")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    bad = df["rating"].isna() | ~df["rating"].isin([1, 2, 3, 4, 5])
    stats["dropped_invalid_rating"] = int(bad.sum())
    df = df[~bad].copy()
    df["rating"] = df["rating"].astype(int)
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce", utc=True).dt.tz_localize(None)
    df["text"] = df["text"].where(df["text"].notna(), None)
    df["text"] = df["text"].map(lambda s: s if s is None else str(s))
    blank = df["text"].fillna("").str.strip().eq("")
    empty = blank & df["review_date"].isna()
    stats["dropped_empty_row"] = int(empty.sum())
    df = df[~empty].copy()
    df["source"] = df["source"].fillna(source)
    df["collected_at"] = df["collected_at"].fillna(collected_at or pd.Timestamp.now("UTC").strftime("%Y-%m-%d"))
    df["language"] = df["language"].fillna("unknown")
    df["has_developer_reply"] = df["has_developer_reply"].map(lambda v: pd.NA if pd.isna(v) else bool(v))
    no_id = df["review_id"].isna() | df["review_id"].astype(str).str.strip().eq("")
    if no_id.any():
        df.loc[no_id, "review_id"] = df[no_id].apply(_make_key, axis=1)
    before = len(df)
    df = df.sort_values("review_date", na_position="first").drop_duplicates("review_id", keep="last")
    stats["dropped_duplicates"] = int(before - len(df))
    stats["missing_text"] = int(df["text"].fillna("").str.strip().eq("").sum())
    stats["missing_date"] = int(df["review_date"].isna().sum())
    stats["missing_version"] = int(df["app_version"].isna().sum())
    df = df[CANONICAL].sort_values("review_date", ascending=False).reset_index(drop=True)
    stats["output_rows"] = int(len(df))
    return df, stats


def merge_with_existing(existing: pd.DataFrame, new: pd.DataFrame) -> pd.DataFrame:
    """Idempotent merge on review_id; newer record wins."""
    if existing is None or len(existing) == 0:
        return new
    both = pd.concat([existing, new], ignore_index=True)
    both["review_date"] = pd.to_datetime(both["review_date"], errors="coerce")
    both = both.drop_duplicates("review_id", keep="last")
    return both.sort_values("review_date", ascending=False).reset_index(drop=True)
