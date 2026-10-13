"""Deterministic metrics. Every percentage carries its denominator."""
from __future__ import annotations
import pandas as pd
from .classify_reviews import CATEGORIES, OTHER, owner_type

NEG_MAX = 2
# Prioritization config: severity weight (1-5) and effort estimate (S/M/L). Both are ANALYST ESTIMATES, not observed.
SEVERITY = {"Crashes, freezing and app stability": 5, "Login, authentication and account access": 5,
            "Booking and cancellation": 4, "Live tracking and GPS accuracy": 4, "Pickup/drop timing and ETA accuracy": 4,
            "Notifications and check-in": 4, "Safety, OTP and driver verification": 5, "Performance, speed and loading": 3,
            "Route planning and pickup order": 3, "Driver, cab and transport operations": 3,
            "Customer support and issue resolution": 3, "UI/UX and navigation": 2, "Permissions and privacy": 3}
EFFORT = {"S": 1, "M": 2, "L": 3}
EFFORT_EST = {"Crashes, freezing and app stability": "M", "Login, authentication and account access": "M",
              "Booking and cancellation": "M", "Live tracking and GPS accuracy": "L", "Pickup/drop timing and ETA accuracy": "L",
              "Notifications and check-in": "M", "Safety, OTP and driver verification": "M", "Performance, speed and loading": "M",
              "Route planning and pickup order": "L", "Driver, cab and transport operations": "L",
              "Customer support and issue resolution": "M", "UI/UX and navigation": "M", "Permissions and privacy": "S"}


def _explode(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["category"] = d["categories"].str.split("|")
    return d.explode("category")


def rating_distribution(df):
    n = len(df)
    c = df["rating"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
    return pd.DataFrame({"rating": c.index, "count": c.values,
                         "pct_of_sample": (c.values / n * 100).round(1) if n else 0.0})


def overview(df) -> dict:
    n = len(df)
    neg = int((df["rating"] <= NEG_MAX).sum()) if n else 0
    d = df["review_date"].dropna()
    return {"n_reviews": n, "sample_mean_rating": round(float(df["rating"].mean()), 2) if n else None,
            "negative_count": neg, "negative_pct": round(neg / n * 100, 1) if n else None,
            "negative_denominator": n,
            "date_min": str(d.min().date()) if len(d) else None, "date_max": str(d.max().date()) if len(d) else None,
            "text_present_pct": round(float(df["text"].fillna("").str.strip().ne("").mean() * 100), 1) if n else None}


def issue_table(df, negative_only=True) -> pd.DataFrame:
    base = df[df["rating"] <= NEG_MAX] if negative_only else df
    den = len(base)
    cols = ["category", "owner_type", "count", "pct_of_denominator", "denominator", "avg_rating"]
    if den == 0:
        return pd.DataFrame(columns=cols)
    ex = _explode(base)
    g = ex.groupby("category").agg(count=("review_id", "nunique"), avg_rating=("rating", "mean")).reset_index()
    g["owner_type"] = g["category"].map(owner_type)
    g["pct_of_denominator"] = (g["count"] / den * 100).round(1)
    g["denominator"] = den
    g["avg_rating"] = g["avg_rating"].round(2)
    return g[cols].sort_values("count", ascending=False).reset_index(drop=True)


def monthly_trend(df, freq="M") -> pd.DataFrame:
    d = df.dropna(subset=["review_date"]).copy()
    if d.empty:
        return pd.DataFrame(columns=["period", "reviews", "negative", "negative_pct", "mean_rating"])
    d["period"] = d["review_date"].dt.to_period(freq).dt.start_time
    g = d.groupby("period").agg(reviews=("review_id", "count"), negative=("rating", lambda s: int((s <= NEG_MAX).sum())),
                                mean_rating=("rating", "mean")).reset_index()
    g["negative_pct"] = (g["negative"] / g["reviews"] * 100).round(1)
    g["mean_rating"] = g["mean_rating"].round(2)
    return g


def version_table(df, min_reviews=10) -> pd.DataFrame:
    d = df.dropna(subset=["app_version"])
    if d.empty:
        return pd.DataFrame(columns=["app_version", "reviews", "negative_pct", "mean_rating"])
    g = d.groupby("app_version").agg(reviews=("review_id", "count"), neg=("rating", lambda s: (s <= NEG_MAX).sum()),
                                     mean_rating=("rating", "mean")).reset_index()
    g["negative_pct"] = (g["neg"] / g["reviews"] * 100).round(1)
    g["mean_rating"] = g["mean_rating"].round(2)
    return g[g["reviews"] >= min_reviews].drop(columns="neg").sort_values("reviews", ascending=False)


def reply_coverage(df) -> dict:
    s = df["has_developer_reply"].dropna()
    if s.empty:
        return {"observable": False}
    neg = df[(df["rating"] <= NEG_MAX) & df["has_developer_reply"].notna()]
    return {"observable": True, "overall_pct": round(float(s.astype(bool).mean() * 100), 1), "overall_denominator": int(len(s)),
            "negative_pct": round(float(neg["has_developer_reply"].astype(bool).mean() * 100), 1) if len(neg) else None,
            "negative_denominator": int(len(neg))}


def classification_coverage(df) -> dict:
    n = len(df)
    if n == 0:
        return {}
    other = df["categories"].eq(OTHER)
    neg = df["rating"] <= NEG_MAX
    return {"classified_pct_all": round(float((~other).mean() * 100), 1),
            "unclassified_negative": int((other & neg).sum()), "negative_total": int(neg.sum()),
            "unclassified_negative_pct": round(float((other & neg).sum() / max(neg.sum(), 1) * 100), 1),
            "multi_label_pct": round(float(df["categories"].str.contains(r"\|").mean() * 100), 1)}


def period_comparison(df, days=30, thresholds=None) -> dict:
    """Latest `days` vs the preceding `days`, anchored on the newest review date. Flags are heuristics."""
    t = {"neg_pct_pp": 10.0, "issue_pp": 8.0, "min_n": 20, **(thresholds or {})}
    d = df.dropna(subset=["review_date"])
    if d.empty:
        return {"available": False, "reason": "no dated reviews", "flags": []}
    end = d["review_date"].max()
    cur = d[d["review_date"] > end - pd.Timedelta(days=days)]
    prev = d[(d["review_date"] <= end - pd.Timedelta(days=days)) & (d["review_date"] > end - pd.Timedelta(days=2 * days))]
    out = {"available": True, "days": days, "anchor_date": str(end.date()), "current_n": len(cur), "previous_n": len(prev), "flags": []}
    if len(cur) < t["min_n"] or len(prev) < t["min_n"]:
        out["available"] = False
        out["reason"] = f"insufficient volume (need >= {t['min_n']} reviews per period; have {len(cur)} and {len(prev)})"
        return out
    cn, pn = (cur["rating"] <= NEG_MAX).mean() * 100, (prev["rating"] <= NEG_MAX).mean() * 100
    out.update(current_neg_pct=round(cn, 1), previous_neg_pct=round(pn, 1), neg_pct_change_pp=round(cn - pn, 1),
               current_mean=round(cur["rating"].mean(), 2), previous_mean=round(prev["rating"].mean(), 2))
    if abs(cn - pn) >= t["neg_pct_pp"]:
        out["flags"].append(f"Negative-review share moved {cn - pn:+.1f} pp ({pn:.1f}% -> {cn:.1f}%)")
    ci, pi = issue_table(cur).set_index("category"), issue_table(prev).set_index("category")
    for cat in ci.index:
        a = ci.loc[cat, "pct_of_denominator"]
        b = pi.loc[cat, "pct_of_denominator"] if cat in pi.index else 0.0
        if a - b >= t["issue_pp"]:
            out["flags"].append(f"'{cat}' share of negative reviews rose {a - b:+.1f} pp ({b:.1f}% -> {a:.1f}%)")
    return out


def prioritize(df) -> pd.DataFrame:
    """Score = frequency% x severity x confidence / effort. Inputs other than frequency are analyst estimates."""
    it = issue_table(df)
    it = it[~it["category"].isin([OTHER, "Positive feedback"])].copy()
    if it.empty:
        return it
    ex = _explode(df[df["rating"] <= NEG_MAX])
    conf_map = {"high": 1.0, "medium": 0.75, "low": 0.5, "none": 0.3}
    cm = ex.groupby("category")["confidence"].apply(lambda s: s.map(conf_map).fillna(0.5).mean())
    it["keyword_confidence"] = it["category"].map(cm).round(2)
    it["severity_est"] = it["category"].map(SEVERITY).fillna(2)
    it["effort_est"] = it["category"].map(EFFORT_EST).fillna("M")
    it["priority_score"] = (it["pct_of_denominator"] * it["severity_est"] * it["keyword_confidence"]
                            / it["effort_est"].map(EFFORT)).round(1)
    return it.sort_values("priority_score", ascending=False).reset_index(drop=True)


def representative_reviews(df, category, n=3, negative_only=True):
    d = df[df["categories"].str.contains(category, regex=False)]
    if negative_only:
        d = d[d["rating"] <= NEG_MAX]
    d = d[d["text"].fillna("").str.len() >= 25]
    cols = ["review_id", "rating", "review_date", "text", "app_version"]
    return d.sort_values(["thumbs_up"], ascending=False, na_position="last").head(n)[cols]
