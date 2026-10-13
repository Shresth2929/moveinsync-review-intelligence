"""Streamlit dashboard. Run: streamlit run app.py"""
import io, json, os
import pandas as pd
import plotly.express as px
import streamlit as st
from src import analyze_reviews as A, classify_reviews as CF, clean_reviews as CL

st.set_page_config(page_title="MoveInSync Review Intelligence", layout="wide")
CAT_PATH, META_PATH = "data/reviews_categorized.csv", "data/collection_meta.json"


@st.cache_data
def load_default():
    if os.path.exists(CAT_PATH):
        return pd.read_csv(CAT_PATH, parse_dates=["review_date"])
    return pd.DataFrame()


def load_meta():
    return json.load(open(META_PATH)) if os.path.exists(META_PATH) else {}


st.title("MoveInSync Review Intelligence")
up = st.sidebar.file_uploader("Or upload a reviews CSV", type="csv")
df = load_default()
meta = load_meta()
qstats = meta.get("clean_stats_last_run", {})
if up is not None:
    clean, qstats = CL.clean_reviews(pd.read_csv(up), source=f"upload:{up.name}")
    df = CF.classify_df(clean)
    meta = {}
if df.empty:
    st.warning("No review data loaded. Run `python -m src.pipeline --collect` or `python -m src.pipeline --import-csv reviews.csv`, "
               "or upload a CSV in the sidebar. No data is shown because none has been collected; nothing is simulated.")
    st.stop()

df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
st.sidebar.header("Filters")
dmin, dmax = df["review_date"].min(), df["review_date"].max()
if pd.notna(dmin):
    rng = st.sidebar.date_input("Date range", (dmin.date(), dmax.date()))
    if isinstance(rng, tuple) and len(rng) == 2:
        keep = df["review_date"].isna() | ((df["review_date"].dt.date >= rng[0]) & (df["review_date"].dt.date <= rng[1]))
        df = df[keep]
ratings = st.sidebar.multiselect("Ratings", [1, 2, 3, 4, 5], default=[1, 2, 3, 4, 5])
df = df[df["rating"].isin(ratings)]
cats = sorted({c for s in df["categories"] for c in s.split("|")})
sel = st.sidebar.multiselect("Category", cats)
if sel:
    df = df[df["categories"].map(lambda s: any(c in s.split("|") for c in sel))]
vers = sorted(df["app_version"].dropna().astype(str).unique())
vsel = st.sidebar.multiselect("App version", vers)
if vsel:
    df = df[df["app_version"].astype(str).isin(vsel)]
if df.empty:
    st.info("No reviews match the filters.")
    st.stop()

ov = A.overview(df)
t1, t2, t3, t4, t5, t6 = st.tabs(["Overview", "Trends", "Root causes", "Prioritization", "Data quality & method", "Exports"])
with t1:
    c = st.columns(4)
    c[0].metric("Displayed Play rating", meta.get("displayed_rating", "n/a"), help=f"Store-wide metric; captured {meta.get('meta_collected_at', 'n/a')}")
    c[1].metric("Reviews analyzed", ov["n_reviews"])
    c[2].metric("Sample mean (written reviews)", ov["sample_mean_rating"])
    c[3].metric("Negative (1-2★) share", f"{ov['negative_pct']}%", help=f"{ov['negative_count']} of {ov['negative_denominator']}")
    st.caption("Displayed rating covers all star ratings; sample mean covers only collected written reviews. They are different metrics.")
    st.plotly_chart(px.bar(A.rating_distribution(df), x="rating", y="count", title=f"Rating distribution (n={len(df)})"), use_container_width=True)
    it = A.issue_table(df)
    if len(it):
        top = it[~it["category"].isin(["Positive feedback"])].head(8)
        st.plotly_chart(px.bar(top, x="pct_of_denominator", y="category", orientation="h",
                               title=f"Share of negative reviews mentioning each theme (denominator = {int(it['denominator'].iloc[0])}; multi-label)"),
                        use_container_width=True)
with t2:
    tr = A.monthly_trend(df)
    if len(tr):
        st.plotly_chart(px.bar(tr, x="period", y="reviews", title="Review volume by month"), use_container_width=True)
        st.plotly_chart(px.line(tr, x="period", y="negative_pct", markers=True, title="Negative review share by month (%)"), use_container_width=True)
    else:
        st.info("No dated reviews.")
    v = A.version_table(df)
    if len(v):
        st.dataframe(v, use_container_width=True)
        st.caption("Versions with >=10 reviews. Differences are descriptive and do not show that a release caused a change.")
    cmp_ = A.period_comparison(df)
    st.write(cmp_)
with t3:
    it = A.issue_table(df)
    st.dataframe(it, use_container_width=True)
    st.caption("Percent = count / negative reviews in the current filter. Multi-label: shares can exceed 100% in total. owner_type: app = software-fixable, ops = operations/support, mixed = both plausible.")
    if len(it):
        pick = st.selectbox("Theme", it["category"])
        st.dataframe(A.representative_reviews(df, pick, n=5, negative_only=False), use_container_width=True)
with t4:
    pr = A.prioritize(df)
    st.dataframe(pr, use_container_width=True)
    st.caption("Priority = frequency % x severity x keyword confidence / effort. Severity and effort are analyst estimates, editable in src/analyze_reviews.py. See reports/executive_recommendations.md for owners, fixes and metrics.")
with t5:
    st.json({"collection": meta.get("collection"), "cleaning_stats": qstats, "classification_coverage": A.classification_coverage(df),
             "developer_reply_coverage": A.reply_coverage(df)})
    st.write("Missing values per column:")
    st.dataframe(df.isna().sum().rename("missing").to_frame())
    st.markdown("Limitations: written reviews are a self-selected sample; keyword rules are imperfect; unofficial scraper may stop working.")
with t6:
    st.download_button("Download categorized CSV (filtered)", df.to_csv(index=False).encode(), "reviews_categorized.csv", "text/csv")
    st.download_button("Download cleaned CSV (filtered)", df[CL.CANONICAL].to_csv(index=False).encode(), "reviews_clean.csv", "text/csv")
    if os.path.exists("reports/executive_recommendations.md"):
        st.download_button("Download executive report (Markdown)", open("reports/executive_recommendations.md", "rb").read(), "executive_recommendations.md")
