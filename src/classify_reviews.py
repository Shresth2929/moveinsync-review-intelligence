"""Transparent, multi-label keyword classifier. Rules are hypotheses and are meant to be edited."""
from __future__ import annotations
import re
import pandas as pd

# category -> (owner_type, regex patterns). owner_type: 'app' (software-fixable) or 'ops' (operations/support/policy) or 'mixed'
CATEGORIES = {
    "Booking and cancellation": ("mixed", [r"\bbook(ing|ed|s)?\b", r"cancel", r"reschedul", r"\bseat\b", r"\broster\b", r"schedule[d]? (a )?(ride|trip|cab)", r"request(ed)? (a )?(ride|cab|trip)", r"no (cab|ride|vehicle) available"]),
    "Login, authentication and account access": (  "app", [r"\blog ?in\b", r"\bsign ?in\b", r"\botp (not|never|doesn)", r"password", r"can'?t (log|sign)", r"unable to (log|sign)", r"account (blocked|locked|not)", r"verification code", r"session expired", r"authenticat"]),
    "Crashes, freezing and app stability": ("app", [r"crash", r"\bfreez", r"keeps? (closing|stopping)", r"force close", r"not (opening|responding)", r"won'?t open", r"\bhang(s|ing)?\b", r"\bbug(s|gy)?\b", r"\bglitch", r"stuck"]),
    "Performance, speed and loading": ("app", [r"\bslow", r"\blag(gy|s|ging)?\b", r"loading", r"takes? (too )?(long|forever|ages)", r"battery", r"heavy app"]),
    "Live tracking and GPS accuracy": ("mixed", [r"\btrack(ing|er)?\b", r"\bgps\b", r"\blocation\b", r"live (map|location)", r"wrong (location|place)", r"cab (location|position)", r"\bmap\b", r"not (updat|refresh)"]),
    "Pickup/drop timing and ETA accuracy": ("mixed", [r"\beta\b", r"\blate\b", r"\bdelay", r"waiting", r"\bwait(ed)?\b", r"on time", r"timing", r"arriv(e|ed|al)", r"never (came|arrived|show)", r"no[- ]?show", r"missed (the )?(cab|bus|ride|pickup)"]),
    "Route planning and pickup order": ("ops", [r"\broute", r"pick ?up order", r"detour", r"long (way|route)", r"\bsequence\b", r"first pick", r"last drop"]),
    "Notifications and check-in": ("app", [r"notif", r"\balert", r"\bremind", r"check[- ]?in", r"check[- ]?out", r"boarding", r"no (message|sms)", r"didn'?t (get|receive) (any )?(message|sms|alert)"]),
    "Safety, OTP and driver verification": ("ops", [r"\bsafe(ty)?\b", r"unsafe", r"\bsos\b", r"panic", r"harass", r"rash", r"\bdriv(es|ing) (fast|badly)", r"verif(y|ied|ication) (of )?(driver|cab)", r"driver (verif|detail|photo)", r"ride otp", r"\botp\b.*(driver|cab|ride)", r"night shift", r"women|female|ladies"]),
    "Driver, cab and transport operations": ("ops", [r"\bdriver", r"\bcab\b", r"\bvehicle", r"\bac\b", r"dirty", r"rude", r"behaviou?r", r"\bfleet", r"\bvan\b", r"\bbus\b", r"overcrowd", r"not (picking|picked|pick)", r"refus"]),
    "UI/UX and navigation": ("app", [r"\bui\b", r"\bux\b", r"interface", r"confus", r"hard to (use|find|navigate)", r"difficult to (use|find)", r"design", r"user[- ]friendly", r"navigat", r"complicated", r"cluttered", r"update(d)? (the )?app.*(worse|bad)"]),
    "Customer support and issue resolution": ("ops", [r"support", r"customer (care|service)", r"no (response|reply)", r"not respond", r"helpline", r"\bcomplain", r"grievance", r"escalat", r"ticket", r"resolv"]),
    "Permissions and privacy": ("app", [r"permission", r"privacy", r"personal (data|info)", r"always[- ]on location", r"background location", r"access to (my )?(contacts|location|phone)"]),
    "Positive feedback": ("n/a", [r"\bgood\b", r"\bgreat\b", r"\bnice\b", r"\bexcellent", r"\bawesome", r"\bbest\b", r"\bhelpful\b", r"love", r"easy to use", r"smooth", r"useful", r"\bperfect"]),
}
OTHER = "Other or insufficient evidence"
NEGATION = re.compile(r"\b(not|no|never|isn'?t|doesn'?t|don'?t|wasn'?t|nothing)\s+(\w+\s+)?(good|great|nice|helpful|useful|smooth|easy)\b", re.I)

_COMPILED = {c: (own, [re.compile(p, re.I) for p in pats]) for c, (own, pats) in CATEGORIES.items()}


def classify_text(text, rating: int):
    """Return dict(categories list, evidence str, confidence str, needs_manual_review bool)."""
    t = "" if text is None or (isinstance(text, float) and pd.isna(text)) else str(text)
    if not t.strip():
        return {"categories": [OTHER], "evidence": "", "confidence": "none", "needs_manual_review": rating <= 2}
    hits, evidence = [], []
    for cat, (_, pats) in _COMPILED.items():
        if cat == "Positive feedback":
            continue
        for p in pats:
            m = p.search(t)
            if m:
                hits.append(cat)
                evidence.append(f"{cat}: '{m.group(0)}'")
                break
    positive = any(p.search(t) for p in _COMPILED["Positive feedback"][1]) and not NEGATION.search(t)
    if positive and (rating >= 4 or not hits):
        if rating >= 4:
            hits.append("Positive feedback")
            m = next(p.search(t) for p in _COMPILED["Positive feedback"][1] if p.search(t))
            evidence.append(f"Positive feedback: '{m.group(0)}'")
    if rating >= 4 and len(hits) > 1 and "Positive feedback" in hits:
        # high-star review with incidental keyword hits (e.g. "good app, driver is nice"): keep positive only
        hits = ["Positive feedback"]
        evidence = [e for e in evidence if e.startswith("Positive")]
    if not hits:
        return {"categories": [OTHER], "evidence": "", "confidence": "low",
                "needs_manual_review": rating <= 2}
    conf = "medium" if len(hits) == 1 and len(evidence) else "low" if len(hits) > 2 else "medium"
    return {"categories": hits, "evidence": "; ".join(evidence), "confidence": conf,
            "needs_manual_review": False}


def classify_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if len(out) == 0:
        for c in ["categories", "evidence", "confidence", "needs_manual_review", "rating_bucket"]:
            out[c] = pd.Series(dtype="object")
        return out
    res = [classify_text(t, r) for t, r in zip(out["text"], out["rating"])]
    out["categories"] = ["|".join(x["categories"]) for x in res]
    out["evidence"] = [x["evidence"] for x in res]
    out["confidence"] = [x["confidence"] for x in res]
    out["needs_manual_review"] = [x["needs_manual_review"] for x in res]
    out["rating_bucket"] = pd.cut(out["rating"], [0, 2, 3, 5], labels=["negative (1-2)", "neutral (3)", "positive (4-5)"]).astype(str)
    return out


def owner_type(cat: str) -> str:
    return CATEGORIES.get(cat, ("n/a", []))[0] if cat != OTHER else "n/a"


def export_validation_sample(df: pd.DataFrame, path: str, n: int = 50, seed: int = 7):
    """Write a random sample for manual labeling (fill 'manual_categories' with '|' separated labels)."""
    s = df.sample(min(n, len(df)), random_state=seed)[["review_id", "rating", "text", "categories"]].copy()
    s["manual_categories"] = ""
    s.to_csv(path, index=False)
    return len(s)


def validation_error_rate(path: str) -> dict:
    """Compare filled manual labels to rule output. Reports exact-match and per-label agreement."""
    v = pd.read_csv(path).dropna(subset=["manual_categories"])
    v = v[v["manual_categories"].astype(str).str.strip() != ""]
    if v.empty:
        return {"labeled": 0, "note": "no manual labels filled in yet"}
    a = v["categories"].map(lambda s: set(str(s).split("|")))
    b = v["manual_categories"].map(lambda s: set(x.strip() for x in str(s).split("|")))
    exact = sum(x == y for x, y in zip(a, b))
    overlap = sum(len(x & y) > 0 for x, y in zip(a, b))
    return {"labeled": int(len(v)), "exact_match": exact, "exact_error_rate": round(1 - exact / len(v), 3),
            "at_least_one_label_agrees": overlap, "no_overlap_rate": round(1 - overlap / len(v), 3)}
