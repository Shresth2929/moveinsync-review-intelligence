"""Collect (unofficial scraper) or import (CSV) Google Play reviews. Never fabricates data.

NOTE: `google-play-scraper` is an UNOFFICIAL, community library that reads Google Play's public web
endpoints. It is NOT an official Google API, may break without notice, and may be subject to Google
Play Terms of Service. The authorized alternative is the Google Play Developer API (reviews.list), which
requires developer-account access to the app, or a CSV export from Play Console.
"""
from __future__ import annotations
import json, os
from datetime import datetime, timezone
import pandas as pd

APP_ID = os.getenv("MIS_APP_ID", "com.moveinsync.ets")
COUNTRY = os.getenv("MIS_COUNTRY", "in")
LANG = os.getenv("MIS_LANG", "en")
MAX_REVIEWS = int(os.getenv("MIS_MAX_REVIEWS", "3000"))


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def collect_from_play(app_id=APP_ID, country=COUNTRY, lang=LANG, max_reviews=MAX_REVIEWS, sort="NEWEST"):
    """Return (reviews_df, app_meta, status). On any failure returns (empty df, {}, status['ok']=False)."""
    status = {"ok": False, "method": "google-play-scraper (unofficial)", "app_id": app_id, "country": country,
              "lang": lang, "sort": sort, "requested_max": max_reviews, "attempted_at": now_iso(), "error": None}
    try:
        from google_play_scraper import app as gp_app, reviews, Sort
        info = gp_app(app_id, lang=lang, country=country)
        meta = {"displayed_rating": info.get("score"), "displayed_ratings_count": info.get("ratings"),
                "displayed_reviews_count": info.get("reviews"), "installs": info.get("installs"),
                "current_version": info.get("version"), "title": info.get("title"),
                "histogram": info.get("histogram"), "meta_collected_at": now_iso()}
        rows, token = [], None
        while len(rows) < max_reviews:
            batch, token = reviews(app_id, lang=lang, country=country, sort=getattr(Sort, sort),
                                   count=min(200, max_reviews - len(rows)), continuation_token=token)
            rows.extend(batch)
            if not token or not batch:
                break
        df = pd.DataFrame(rows)
        if df.empty:
            raise RuntimeError("Scraper returned zero reviews")
        df = df.drop(columns=[c for c in ("userName", "userImage") if c in df.columns])
        df["source"] = f"google_play_scraper:{country}:{lang}:{sort.lower()}"
        df["language"] = lang
        df["collected_at"] = now_iso()[:10]
        status.update(ok=True, fetched_rows=int(len(df)))
        return df, meta, status
    except Exception as e:  # network failure, rate limit, library breakage
        status["error"] = f"{type(e).__name__}: {e}"[:500]
        return pd.DataFrame(), {}, status


def import_csv(path: str, source: str | None = None) -> pd.DataFrame:
    """Import a CSV exported from Play Console or another legitimate source. Columns are auto-mapped."""
    df = pd.read_csv(path, encoding="utf-8", encoding_errors="replace")
    df["source"] = source or f"csv_import:{os.path.basename(path)}"
    return df


def save_json(obj, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)
