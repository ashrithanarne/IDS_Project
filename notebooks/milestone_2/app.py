import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

st.set_page_config(page_title="Humanitarian Media Dashboard", layout="wide")

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    conn = sqlite3.connect("humanitarian.db")
    crises_df    = pd.read_sql("SELECT * FROM crises", conn)
    monthly_df   = pd.read_sql("SELECT * FROM monthly_coverage", conn)
    outlet_df    = pd.read_sql("SELECT * FROM coverage_by_outlet", conn)
    framing_df   = pd.read_sql("SELECT * FROM framing", conn)
    sentiment_df = pd.read_sql("SELECT * FROM sentiment", conn)
    conn.close()
    monthly_df["year_month"] = pd.to_datetime(monthly_df["year_month"])
    name_map = crises_df.set_index("crisis_id")["crisis_name"].to_dict()
    monthly_df["crisis_name"] = monthly_df["crisis_id"].map(name_map)
    outlet_df["crisis_name"]  = outlet_df["crisis_id"].map(name_map)
    return crises_df, monthly_df, outlet_df, framing_df, sentiment_df

crises_df, monthly_df, outlet_df, framing_df, sentiment_df = load_data()

CRISIS_COLORS = ["#E63946","#457B9D","#2A9D8F","#E9C46A","#F4A261","#264653","#6A4C93","#1D7874","#A8DADC","#C77DFF"]

st.title("Humanitarian Media Coverage Dashboard")

# ── Sidebar nav ────────────────────────────────────────────────────────────────
section = st.sidebar.radio("Section", [
    "1 · Coverage Landscape",
    "2 · Severity vs Coverage",
    "3 · Monthly Timeline",
    "4 · Outlet Analysis",
    "5 · Framing & Sentiment",
    "6 · Model Results",
])

# ── Section 1 ──────────────────────────────────────────────────────────────────
if section == "1 · Coverage Landscape":
    metric = st.radio("Metric", {
        "Total Articles": "raw_coverage",
        "Articles per Day": "coverage_per_day",
        "Per Funding Unit": "coverage_per_funding",
        "Per Person Affected": "coverage_per_people",
    }.keys(), horizontal=True)
    col = {"Total Articles":"raw_coverage","Articles per Day":"coverage_per_day",
           "Per Funding Unit":"coverage_per_funding","Per Person Affected":"coverage_per_people"}[metric]
    sorted_df = crises_df.sort_values(col, ascending=True)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.barh(sorted_df["crisis_name"], sorted_df[col], color=CRISIS_COLORS[:len(sorted_df)], edgecolor="white")
    ax.set_xlabel(metric); ax.set_title(f"Coverage Landscape — {metric}")
    st.pyplot(fig)

# ── Section 2 ──────────────────────────────────────────────────────────────────
elif section == "2 · Severity vs Coverage":
    sev = st.radio("Severity metric", ["People Affected","Funds Required","Crisis Duration (days)"], horizontal=True)
    col = {"People Affected":"people_affected","Funds Required":"fund_required","Crisis Duration (days)":"crisis_days"}[sev]
    fig, ax = plt.subplots(figsize=(9,5))
    for i, row in crises_df.iterrows():
        ax.scatter(row[col], row["raw_coverage"], s=130, color=CRISIS_COLORS[i%len(CRISIS_COLORS)], edgecolors="white", zorder=3)
        ax.annotate(row["crisis_name"], (row[col], row["raw_coverage"]), xytext=(8,4), textcoords="offset points", fontsize=8)
    x = crises_df[col].values; y = crises_df["raw_coverage"].values
    m,b = np.polyfit(x,y,1)
    ax.plot([x.min(),x.max()],[m*x.min()+b,m*x.max()+b],"--",color="#999",linewidth=1.5)
    ax.set_xlabel(sev); ax.set_ylabel("Total Articles"); ax.set_title(f"Coverage vs {sev}")
    st.pyplot(fig)

# ── Section 3 ──────────────────────────────────────────────────────────────────
elif section == "3 · Monthly Timeline":
    all_crises = sorted(monthly_df["crisis_name"].dropna().unique())
    selected = st.multiselect("Select crises", all_crises, default=all_crises[:5])
    smooth = st.checkbox("3-month rolling average", value=True)
    if selected:
        fig, ax = plt.subplots(figsize=(12,5))
        for idx, crisis in enumerate(selected):
            s = monthly_df[monthly_df["crisis_name"]==crisis].set_index("year_month")["coverage_count"].sort_index()
            color = CRISIS_COLORS[idx % len(CRISIS_COLORS)]
            ax.fill_between(s.index, s.values, alpha=0.08, color=color)
            vals = s.rolling(3, center=True, min_periods=1).mean() if smooth and len(s)>=3 else s
            ax.plot(vals.index, vals.values, linewidth=2, color=color, label=crisis)
        ax.legend(fontsize=9); ax.set_title("Monthly Coverage Timeline")
        plt.xticks(rotation=35, fontsize=8)
        st.pyplot(fig)

# ── Section 4 ──────────────────────────────────────────────────────────────────
elif section == "4 · Outlet Analysis":
    view = st.radio("View", ["Global Top Outlets", "Outlet Concentration"], horizontal=True)
    if view == "Global Top Outlets":
        top = outlet_df.groupby("outlet_name")["coverage_count"].sum().sort_values(ascending=True).tail(12)
        fig, ax = plt.subplots(figsize=(10,5))
        colors = ["#E63946" if i==len(top)-1 else "#457B9D" for i in range(len(top))]
        ax.barh(top.index, top.values, color=colors, edgecolor="white")
        ax.set_title("Global Top Outlets"); st.pyplot(fig)
    else:
        crisis_filter = st.selectbox("Crisis", sorted(outlet_df["crisis_name"].dropna().unique()))
        sub = outlet_df[outlet_df["crisis_name"]==crisis_filter].sort_values("coverage_count",ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10,4))
        ax.bar(sub["outlet_name"], sub["coverage_count"], color="#457B9D", edgecolor="white")
        plt.xticks(rotation=35, ha="right", fontsize=8); ax.set_title(f"Top Outlets — {crisis_filter}")
        st.pyplot(fig)

# ── Section 5 ──────────────────────────────────────────────────────────────────
elif section == "5 · Framing & Sentiment":
    col1, col2 = st.columns(2)
    with col1:
        f_counts = framing_df.groupby("framing_type")["raw_count"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots()
        ax.pie(f_counts.values, labels=f_counts.index, autopct="%1.0f%%", startangle=140,
               colors=["#E63946","#457B9D","#2A9D8F","#E9C46A","#F4A261"])
        ax.set_title("Framing Distribution"); st.pyplot(fig)
    with col2:
        if "entity_name" in sentiment_df.columns:
            ent = sentiment_df.groupby("entity_name")["sentiment_score"].mean().sort_values()
            fig, ax = plt.subplots()
            colors = ["#E63946" if v<0 else "#2A9D8F" for v in ent.values]
            ax.barh(ent.index, ent.values, color=colors, edgecolor="white")
            ax.axvline(0, color="#333", linewidth=0.8); ax.set_title("Entity Sentiment")
            st.pyplot(fig)

# ── Section 6 ──────────────────────────────────────────────────────────────────
elif section == "6 · Model Results":
    st.info("Refit models on your model_df here — replace with your actual feature columns.")