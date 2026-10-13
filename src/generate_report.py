"""Generate the data-driven executive report. All numbers come from the dataset; none are hardcoded."""
from __future__ import annotations
import json, os
import pandas as pd
from . import analyze_reviews as A

PROPOSED = {  # hypotheses + proposed fixes (analyst-authored templates; must be validated against evidence shown)
 "Crashes, freezing and app stability": ("Mobile engineering", "Pull crash clusters from Play Console Android Vitals / Crashlytics for the app versions named in reviews; reproduce top stack traces; ship a hotfix for top-3 clusters.", "Crash-free sessions; ANR rate (needs internal access)"),
 "Login, authentication and account access": ("Backend + Mobile engineering", "Audit login/OTP/session failure logs; add clear error states and retry; verify SMS/OTP delivery provider success rates.", "Login success rate (needs internal access)"),
 "Booking and cancellation": ("Product + Backend", "Review booking/cancellation funnel drop-offs; surface cut-off rules and failure reasons inside the app; reduce steps to book/cancel.", "Booking completion rate; cancellation-failure rate (needs internal access)"),
 "Live tracking and GPS accuracy": ("Mobile + Backend", "Compare reported vehicle position with driver-app GPS pings; inspect update interval/staleness; add 'last updated' timestamp.", "Position staleness p95; tracking-related complaint share"),
 "Pickup/drop timing and ETA accuracy": ("Backend + Operations", "Measure ETA vs actual arrival error; separate algorithm error from late operations; show confidence/ETA ranges.", "ETA absolute error p50/p90 (needs internal access)"),
 "Notifications and check-in": ("Mobile + Backend", "Audit push delivery (FCM) and notification settings flows; handle OEM battery-optimisation kills; add fallback SMS for critical alerts.", "Push delivery/open rate (needs internal access)"),
 "Safety, OTP and driver verification": ("Operations + Product", "Triage safety-tagged reviews manually within 48h; confirm driver verification and OTP flows work end-to-end.", "Safety incident reports per 10k trips (needs internal access)"),
 "Performance, speed and loading": ("Mobile engineering", "Profile cold start and key screens; cache roster/trip data; measure on low-end devices.", "Cold-start time p90; screen load p90"),
 "Route planning and pickup order": ("Operations", "Review routing rules and pickup sequence complaints with routing team; communicate sequence changes in advance.", "Route-related complaint share"),
 "Driver, cab and transport operations": ("Operations", "Route to fleet/vendor management; this is mainly NOT an app defect.", "Operations NPS / vendor SLA (needs internal access)"),
 "Customer support and issue resolution": ("Support", "Measure first-response and resolution time; add in-app issue reporting with ticket status; reply to negative reviews.", "First-response time; developer-reply coverage"),
 "UI/UX and navigation": ("Product design", "Run usability review on top-complaint flows after defects are fixed.", "Task completion rate in usability tests"),
 "Permissions and privacy": ("Product + Legal", "Review permission prompts and privacy copy; request only needed permissions.", "Permission-denial rate"),
}


def build_report(df: pd.DataFrame, meta: dict, coll: dict, qstats: dict, out_path: str) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    n = len(df)
    L = []
    if n == 0:
        L += ["# Executive Recommendations — NO REAL DATA ANALYZED", "",
              "**Status:** No review dataset is present. The report intentionally contains no findings.", "",
              f"**Collection attempt:** {json.dumps(coll, default=str)}", "",
              "To produce the real report: provide data via `python -m src.pipeline --import-csv <file>` or re-run "
              "`python -m src.pipeline --collect` from a machine that can reach Google Play. See README."]
        open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
        return out_path
    ov, dist = A.overview(df), A.rating_distribution(df)
    it, pr = A.issue_table(df), A.prioritize(df)
    cov, rc, cmp_ = A.classification_coverage(df), A.reply_coverage(df), A.period_comparison(df)
    disp = meta.get("displayed_rating")
    L += ["# MoveInSync Review Intelligence — Executive Recommendations", "",
          f"*Dataset: {n} written reviews, {ov['date_min']} to {ov['date_max']}. Source: {df['source'].iloc[0]}. Collected: {meta.get('meta_collected_at') or df['collected_at'].max()}.*", "",
          "## 1. Executive summary", "",
          f"- **Displayed Google Play rating:** {disp if disp is not None else 'not captured in this dataset'} (store-wide, all star ratings). **Sample mean of written reviews:** {ov['sample_mean_rating']} (n={n}). These are different metrics.",
          f"- **Negative reviews (1–2★):** {ov['negative_count']} of {ov['negative_denominator']} sampled reviews ({ov['negative_pct']}%).",
          ]
    top = pr.head(3)
    for _, r in top.iterrows():
        L.append(f"- **{r['category']}** appears in {r['count']} of {r['denominator']} negative reviews ({r['pct_of_denominator']}%); owner type: {r['owner_type']}.")
    L += ["", "Percentages are keyword-rule matches, multi-label (can sum above 100%). Causes below are hypotheses until confirmed with internal telemetry.", "",
          "## 2. Research question and scope", "",
          "Why are Play Store ratings for the MoveInSync employee transport app poor, and what should Product and Engineering fix first? Scope: public written reviews only.", "",
          "## 3. Data sources, collection and sample", "",
          f"- Collection method/status: `{coll.get('method', 'n/a')}`; country `{coll.get('country', 'n/a')}`, language `{coll.get('lang', 'n/a')}`, sort `{coll.get('sort', 'n/a')}`.",
          f"- Cleaning: {json.dumps(qstats)}",
          "- Selection bias: only users who chose to write a review are included; written reviews skew towards strong opinions and are not representative of all employees or rides.", "",
          "## 4. Rating and negative-review evidence", "", f"| Rating | Count | % of sample (n={n}) |", "|---|---|---|"]
    L += [f"| {int(r.rating)}★ | {int(r['count'])} | {r.pct_of_sample}% |" for _, r in dist.iterrows()]
    if cmp_.get("available"):
        L += ["", f"Period comparison (last {cmp_['days']} days vs previous {cmp_['days']}, anchored {cmp_['anchor_date']}): negative share {cmp_['previous_neg_pct']}% → {cmp_['current_neg_pct']}% (n={cmp_['previous_n']} → {cmp_['current_n']})."]
    else:
        L += ["", f"Period comparison not available: {cmp_.get('reason')}."]
    L += ["", "## 5. Top complaint themes (denominator = %d negative reviews)" % ov["negative_count"], "",
          "| Theme | Owner type | Count | % of negative |", "|---|---|---|---|"]
    L += [f"| {r['category']} | {r['owner_type']} | {r['count']} | {r['pct_of_denominator']}% |" for _, r in it.iterrows()]
    L += ["", "## 6. Representative review evidence", ""]
    for _, r in pr.head(5).iterrows():
        L.append(f"**{r['category']}**")
        for _, x in A.representative_reviews(df, r["category"]).iterrows():
            txt = str(x["text"]).replace("\n", " ")[:300]
            L.append(f"- [{x['review_id']}] {int(x['rating'])}★, {str(x['review_date'])[:10]}: “{txt}”")
        L.append("")
    L += ["## 7. Root causes vs hypotheses", "",
          "Review text alone cannot prove root cause. Every item below is a **hypothesis** with keyword-level evidence; confirmation requires crash, funnel, GPS and notification telemetry from MoveInSync.", "",
          "## 8. Prioritized fixes and owners", "",
          "Priority score = frequency % × severity (analyst estimate 1–5) × keyword confidence ÷ effort (S=1, M=2, L=3; analyst estimate).", "",
          "| # | Theme | Share of negative | Score | Owner | Effort (est.) | Proposed fix | Success metric |", "|---|---|---|---|---|---|---|---|"]
    for i, (_, r) in enumerate(pr.iterrows(), 1):
        o, fix, metric = PROPOSED.get(r["category"], ("TBD", "TBD", "TBD"))
        L.append(f"| {i} | {r['category']} | {r['pct_of_denominator']}% ({r['count']}/{r['denominator']}) | {r['priority_score']} | {o} | {r['effort_est']} | {fix} | {metric} |")
    L += ["", "Baselines for each metric must come from internal data; targets are to be set by the team and are not predictions.", "",
          "## 9. Action plan", "",
          "- **First 48 hours:** reproduce the top-3 themes on real devices; pull crash/login/funnel logs for the versions named in reviews; manually triage any safety-tagged reviews.",
          "- **Weeks 1–2:** ship fixes for the highest-confidence app-side defects; reply to negative reviews with specifics; validate via staged rollout.",
          "- **Days 30:** monitor negative-review share and theme shares with the recurring pipeline; check for regressions per release.",
          "- **Ongoing:** weekly pipeline run; investigate flags.", "",
          "## 10. Metrics and validation", "",
          "Crash-free sessions, login success, booking completion, ETA error, notification delivery, issue recurrence, negative-review share. Most require internal access. Review-based metrics are measured by this pipeline.", "",
          "## 11. Risks, assumptions and limitations", "",
          "- Keyword classification is imprecise; see `reports/methodology.md` for the validation procedure. Classification coverage: %s%% of reviews matched a category; %s%% of negative reviews unclassified." % (cov.get("classified_pct_all"), cov.get("unclassified_negative_pct")),
          f"- Reply coverage: {rc}", "- No causal claims about releases are made.", "",
          "## 12. Recurring monitoring", "", "`python -m src.pipeline --collect` (or `--import-csv`) weekly; flags are written to `data/latest_flags.json`.", ""]
    if cmp_.get("flags"):
        L += ["**Current flags:** " + "; ".join(cmp_["flags"]), ""]
    L += ["## 13. Tools and methodology", "", "Python, pandas, Streamlit, Plotly, pytest; unofficial google-play-scraper or CSV import; rule-based classification; no LLM used.", ""]
    open(out_path, "w", encoding="utf-8").write("\n".join(L))
    return out_path
