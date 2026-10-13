"""CLI: python -m src.pipeline [--collect | --import-csv FILE] [--report] [--validation-sample]"""
from __future__ import annotations
import argparse, json, os, sys
import pandas as pd
from . import collect_reviews as C, clean_reviews as CL, classify_reviews as CF, analyze_reviews as A, generate_report as G

D = "data"; R = "reports"
RAW, CLEAN, CAT = f"{D}/reviews_clean.csv", f"{D}/reviews_clean.csv", f"{D}/reviews_categorized.csv"


def _load(path):
    return pd.read_csv(path, parse_dates=["review_date"]) if os.path.exists(path) else pd.DataFrame()


def run(args) -> int:
    os.makedirs(D, exist_ok=True); os.makedirs(R, exist_ok=True)
    meta = json.load(open(f"{D}/collection_meta.json")) if os.path.exists(f"{D}/collection_meta.json") else {}
    coll = meta.get("collection", {})
    new = None
    if args.collect:
        df, app_meta, status = C.collect_from_play()
        coll = status
        if status["ok"]:
            new, stats = CL.clean_reviews(df, collected_at=C.now_iso()[:10])
            meta.update(app_meta)
        else:
            print(f"COLLECTION FAILED: {status['error']}\nExisting data preserved. Use --import-csv as fallback.", file=sys.stderr)
    if args.import_csv:
        df = C.import_csv(args.import_csv)
        new, stats = CL.clean_reviews(df, source=f"csv_import:{os.path.basename(args.import_csv)}")
        coll = {"ok": True, "method": f"CSV import ({os.path.basename(args.import_csv)})", "attempted_at": C.now_iso(),
                "country": "n/a", "lang": "n/a", "sort": "n/a"}
        meta.setdefault("displayed_rating", args.displayed_rating)
        if args.displayed_rating is not None:
            meta["displayed_rating"] = args.displayed_rating; meta["meta_collected_at"] = C.now_iso()
    existing = _load(CLEAN)
    if new is not None:
        merged = CL.merge_with_existing(existing, new)
        merged.to_csv(CLEAN, index=False)
        meta["clean_stats_last_run"] = stats
        existing = merged
    meta["collection"] = coll
    C.save_json(meta, f"{D}/collection_meta.json")
    df = _load(CLEAN)
    cat = CF.classify_df(df) if len(df) else df
    if len(cat):
        cat.to_csv(CAT, index=False)
        cmp_ = A.period_comparison(cat)
        C.save_json({"generated": C.now_iso(), **cmp_}, f"{D}/latest_flags.json")
        if args.validation_sample:
            print("validation sample rows:", CF.export_validation_sample(cat, f"{D}/validation_sample.csv"))
    G.build_report(cat if len(cat) else pd.DataFrame(), meta, coll, meta.get("clean_stats_last_run", {}), f"{R}/executive_recommendations.md")
    print(f"rows in dataset: {len(df)}; report: {R}/executive_recommendations.md")
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--collect", action="store_true", help="collect from Google Play via unofficial scraper")
    p.add_argument("--import-csv", help="import reviews from a CSV file")
    p.add_argument("--displayed-rating", type=float, help="displayed Play Store rating (manual entry for CSV imports)")
    p.add_argument("--validation-sample", action="store_true", help="write data/validation_sample.csv for manual labeling")
    sys.exit(run(p.parse_args()))


if __name__ == "__main__":
    main()
