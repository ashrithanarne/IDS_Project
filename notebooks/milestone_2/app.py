"""
Humanitarian Media Coverage Dashboard
Reads from CSV files in data/raw/ and data/processed/.

Project layout — run from notebooks/milestone_2/:
  IDS_Project/
    data/
      raw/
        chart1_overall_coverage_bar.csv
        chart3_monthly_coverage.csv
        chart4_crisis_coverage_per_outlet_chart.csv
        framing_per_article.csv
        sentiment_per_article.csv
      processed/
        monthly_model_data.csv
    notebooks/
      milestone_2/app.py   ← this file

Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

st.set_page_config(page_title="Humanitarian Media Dashboard", layout="wide")

# ── Colour palettes ────────────────────────────────────────────────────────────
CRISIS_COLORS = ["#E63946","#457B9D","#2A9D8F","#E9C46A","#F4A261",
                 "#264653","#6A4C93","#1D7874","#A8DADC","#C77DFF"]
FRAME_COLORS  = ["#E63946","#457B9D","#2A9D8F","#E9C46A","#F4A261","#A8DADC"]
SENT_PAL      = {"positive":"#2A9D8F","neutral":"#9E9E9E","negative":"#E63946"}

plt.rcParams.update({
    "figure.facecolor":"#FAFAFA","axes.facecolor":"#FAFAFA",
    "axes.spines.top":False,"axes.spines.right":False,
    "axes.grid":True,"grid.alpha":0.3,"grid.linestyle":"--"
})

# ── Resolve paths relative to this script ─────────────────────────────────────
_HERE    = os.path.dirname(os.path.abspath(__file__))
RAW_DIR  = os.path.join(_HERE, "..", "..", "data", "raw")
CSV_PATH = os.path.join(_HERE, "..", "..", "data", "processed", "monthly_model_data.csv")

# ── Load CSV tables ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    crises_df    = pd.read_csv(os.path.join(RAW_DIR, "chart1_overall_coverage_bar.csv"))
    monthly_df   = pd.read_csv(os.path.join(RAW_DIR, "chart3_monthly_coverage.csv"))
    outlet_df    = pd.read_csv(os.path.join(RAW_DIR, "chart4_crisis_coverage_per_outlet_chart.csv"))
    framing_df   = pd.read_csv(os.path.join(RAW_DIR, "framing_per_article.csv"))
    sentiment_df = pd.read_csv(os.path.join(RAW_DIR, "sentiment_per_article.csv"))

    if "year_month" in monthly_df.columns:
        monthly_df["year_month"] = pd.to_datetime(monthly_df["year_month"])

    # Map crisis_id -> crisis_name where applicable
    if "crisis_id" in crises_df.columns and "crisis_name" in crises_df.columns:
        name_map = crises_df.set_index("crisis_id")["crisis_name"].to_dict()
        for df in [monthly_df, outlet_df, framing_df]:
            if "crisis_id" in df.columns and "crisis_name" not in df.columns:
                df["crisis_name"] = df["crisis_id"].map(name_map)

    return crises_df, monthly_df, outlet_df, framing_df, sentiment_df

crises_df, monthly_df, outlet_df, framing_df, sentiment_df = load_data()

# ── Load model CSV (falls back to DB-derived data if CSV missing) ──────────────
@st.cache_data
def load_model_df():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        if "year_month" in df.columns:
            df["year_month"] = pd.to_datetime(df["year_month"])
        return df
    # Fallback: derive from monthly + crises data
    df = monthly_df.copy()
    if "crisis_id" in df.columns and "crisis_id" in crises_df.columns:
        merge_cols = ["crisis_id"] + [
            c for c in ["fund_required","people_affected","crisis_days","raw_coverage"]
            if c in crises_df.columns
        ]
        df = df.merge(crises_df[merge_cols], on="crisis_id", how="left")
    if "year_month" in df.columns:
        df["month_num"] = (
            df["year_month"].dt.year - 2015
        ) * 12 + df["year_month"].dt.month
        df["onset"] = (
            df.groupby("crisis_id")["month_num"].transform(lambda x: (x - x.min()) < 3)
        ).astype(int)
    if "coverage_count" in outlet_df.columns and "crisis_id" in outlet_df.columns:
        hhi = (
            outlet_df.groupby("crisis_id")
            .apply(lambda g: ((g["coverage_count"] / g["coverage_count"].sum())**2).sum())
            .reset_index(name="outlet_hhi")
        )
        df = df.merge(hhi, on="crisis_id", how="left")
    return df.dropna()

model_df = load_model_df()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.title("Humanitarian Media Coverage Dashboard")
st.caption(
    "International media coverage of humanitarian crises 2015-2024  ·  "
    "Key finding: coverage is driven by framing, not severity."
)

section = st.sidebar.radio("Section", [
    "1 · Coverage Landscape",
    "2 · Severity vs Coverage",
    "3 · Monthly Timeline",
    "4 · Outlet Analysis",
    "5 · Framing & Sentiment",
    "6 · Model Results",
])

# ═══════════════════════════════════════════════════════════════════════════════
# 1 · Coverage Landscape
# ═══════════════════════════════════════════════════════════════════════════════
if section == "1 · Coverage Landscape":
    st.subheader("Crisis Coverage Landscape")
    st.markdown("Which crises received the most media attention, and does it reflect their severity?")

    # Determine which metric columns are available
    metric_options = {
        "Total Articles":      "raw_coverage",
        "Articles per Day":    "coverage_per_day",
        "Per Funding Unit":    "coverage_per_funding",
        "Per Person Affected": "coverage_per_people",
    }
    available_metrics = {k: v for k, v in metric_options.items() if v in crises_df.columns}

    if not available_metrics:
        st.error("No coverage metric columns found in chart1_overall_coverage_bar.csv.")
        st.stop()

    metric = st.radio("Metric", list(available_metrics.keys()), horizontal=True)
    col = available_metrics[metric]

    sorted_df = crises_df.sort_values(col, ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(
        sorted_df["crisis_name"], sorted_df[col],
        color=CRISIS_COLORS[:len(sorted_df)], edgecolor="white", height=0.65
    )
    for bar, val in zip(bars, sorted_df[col]):
        ax.text(
            bar.get_width() + sorted_df[col].max() * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,.1f}", va="center", fontsize=9, color="#333"
        )
    ax.set_xlabel(metric)
    ax.set_title(f"Coverage Landscape — {metric}", pad=14)
    ax.set_xlim(0, sorted_df[col].max() * 1.14)
    ax.tick_params(axis="y", labelsize=10)
    plt.tight_layout()
    st.pyplot(fig)
    st.info(
        "**Insight:** Gaza leads across all four metrics — including per person affected and "
        "per funding unit — suggesting something beyond humanitarian severity is driving attention."
    )

# ═══════════════════════════════════════════════════════════════════════════════
# 2 · Severity vs Coverage
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "2 · Severity vs Coverage":
    st.subheader("Coverage vs. Crisis Severity")
    st.markdown("Does humanitarian severity predict media attention?")

    sev_options = {
        "People Affected":        "people_affected",
        "Funds Required":         "fund_required",
        "Crisis Duration (days)": "crisis_days",
    }
    available_sev = {k: v for k, v in sev_options.items() if v in crises_df.columns}

    if not available_sev:
        st.error("No severity columns (people_affected, fund_required, crisis_days) found in the crises CSV.")
        st.stop()

    sev = st.radio("Severity metric", list(available_sev.keys()), horizontal=True)
    col = available_sev[sev]

    if "raw_coverage" not in crises_df.columns:
        st.error("`raw_coverage` column not found in crises CSV.")
        st.stop()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for i, row in crises_df.iterrows():
        ax.scatter(
            row[col], row["raw_coverage"], s=130,
            color=CRISIS_COLORS[i % len(CRISIS_COLORS)],
            edgecolors="white", linewidths=1.2, zorder=3
        )
        ax.annotate(
            row["crisis_name"], (row[col], row["raw_coverage"]),
            xytext=(8, 4), textcoords="offset points", fontsize=8.5, color="#333"
        )
    x_v = crises_df[col].values.reshape(-1, 1)
    y_v = crises_df["raw_coverage"].values
    lr  = LinearRegression().fit(x_v, y_v)
    x_line = np.linspace(x_v.min(), x_v.max(), 100).reshape(-1, 1)
    ax.plot(x_line, lr.predict(x_line), "--", color="#999", linewidth=1.5, label="Linear trend")
    r2 = r2_score(y_v, lr.predict(x_v))
    ax.set_title(f"Raw Coverage vs {sev}   (R² = {r2:.3f})", pad=12)
    ax.set_xlabel(sev)
    ax.set_ylabel("Total Articles")
    ax.legend(fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    st.info("**Insight:** Low R² values confirm that severity metrics alone do not predict coverage volume.")

# ═══════════════════════════════════════════════════════════════════════════════
# 3 · Monthly Timeline
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "3 · Monthly Timeline":
    st.subheader("Monthly Coverage Timeline")

    if "crisis_name" not in monthly_df.columns:
        st.error("`crisis_name` column not found in monthly coverage CSV.")
        st.stop()

    all_crises = sorted(monthly_df["crisis_name"].dropna().unique())
    selected   = st.multiselect("Select crises", all_crises, default=all_crises[:5])
    smooth     = st.checkbox("3-month rolling average", value=True)

    count_col = "coverage_count" if "coverage_count" in monthly_df.columns else monthly_df.select_dtypes("number").columns[0]

    if selected:
        fig, ax = plt.subplots(figsize=(12, 5))
        for idx, crisis in enumerate(selected):
            s = (monthly_df[monthly_df["crisis_name"] == crisis]
                 .set_index("year_month")[count_col].sort_index())
            color = CRISIS_COLORS[idx % len(CRISIS_COLORS)]
            vals  = s.rolling(3, center=True, min_periods=1).mean() if smooth and len(s) >= 3 else s
            ax.fill_between(vals.index, vals.values, alpha=0.08, color=color)
            ax.plot(vals.index, vals.values, linewidth=2, color=color, label=crisis)
        ax.legend(fontsize=9)
        ax.set_title("Monthly Coverage Timeline")
        ax.set_ylabel("Articles")
        plt.xticks(rotation=35, fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)

# ═══════════════════════════════════════════════════════════════════════════════
# 4 · Outlet Analysis
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "4 · Outlet Analysis":
    st.subheader("Outlet Analysis")
    view = st.radio("View", ["Global Top Outlets", "Outlet Concentration"], horizontal=True)

    outlet_name_col  = "outlet_name"  if "outlet_name"  in outlet_df.columns else outlet_df.columns[0]
    outlet_count_col = "coverage_count" if "coverage_count" in outlet_df.columns else outlet_df.select_dtypes("number").columns[0]

    if view == "Global Top Outlets":
        top = (outlet_df.groupby(outlet_name_col)[outlet_count_col]
               .sum().sort_values(ascending=True).tail(12))
        fig, ax = plt.subplots(figsize=(10, 5))
        bar_colors = ["#E63946" if i == len(top)-1 else "#457B9D" for i in range(len(top))]
        ax.barh(top.index, top.values, color=bar_colors, edgecolor="white")
        ax.set_title("Global Top Outlets by Total Articles")
        ax.set_xlabel("Articles")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        # Top-3 outlet share per crisis — matches notebook widget
        if "crisis_name" not in outlet_df.columns:
            st.error("`crisis_name` not found in outlet CSV.")
        else:
            crisis_conc = []
            for crisis, grp in outlet_df.groupby("crisis_name"):
                total = grp[outlet_count_col].sum()
                if total == 0:
                    continue
                top3_share = grp[outlet_count_col].nlargest(3).sum() / total
                crisis_conc.append({"crisis_name": crisis, "top3_share": top3_share})
            
            conc_df = pd.DataFrame(crisis_conc).sort_values("top3_share", ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            bar_colors = ["#E63946" if v >= 0.7 else "#457B9D" for v in conc_df["top3_share"]]
            bars = ax.bar(conc_df["crisis_name"], conc_df["top3_share"],
                          color=bar_colors, edgecolor="white")
            ax.axhline(0.7, color="#E63946", linestyle="--", linewidth=1.5,
                       label="High concentration threshold (70%)")
            for bar, val in zip(bars, conc_df["top3_share"]):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f"{val:.0%}", ha="center", fontsize=9)
            ax.set_title("Top-3 Outlet Share of Coverage per Crisis")
            ax.set_ylabel("Proportion of Total Articles")
            ax.set_ylim(0, 1.05)
            ax.legend(fontsize=9)
            plt.xticks(rotation=30, ha="right", fontsize=9)
            plt.tight_layout()
            st.pyplot(fig)

# ═══════════════════════════════════════════════════════════════════════════════
# 5 · Framing & Sentiment
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "5 · Framing & Sentiment":
    st.subheader("Framing & Sentiment")

    framing_type_col = "framing_type" if "framing_type" in framing_df.columns else framing_df.columns[1]
    framing_count_col = "raw_count" if "raw_count" in framing_df.columns else framing_df.select_dtypes("number").columns[0]

    framing_view = st.radio(
        "Framing view",
        ["Global Distribution", "Per-Crisis Stacked Bar", "Framing vs Coverage (scatter)"],
        horizontal=True
    )

    if framing_view == "Global Distribution":
        counts = framing_df.groupby(framing_type_col)[framing_count_col].sum().sort_values(ascending=False)
        c1, c2 = st.columns(2)
        with c1:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(counts.index, counts.values,
                   color=FRAME_COLORS[:len(counts)], edgecolor="white")
            ax.set_title("Articles by Framing Type")
            ax.set_ylabel("Total Articles")
            plt.xticks(rotation=30, fontsize=9)
            for i, (k, v) in enumerate(counts.items()):
                ax.text(i, v + counts.max()*0.01, f"{v:,}", ha="center", fontsize=9)
            plt.tight_layout()
            st.pyplot(fig)
        with c2:
            fig, ax = plt.subplots(figsize=(5, 4))
            wedges, texts, autotexts = ax.pie(
                counts.values, labels=counts.index,
                colors=FRAME_COLORS[:len(counts)],
                autopct="%1.0f%%", startangle=140,
                wedgeprops={"edgecolor":"white","linewidth":1.5},
                pctdistance=0.78
            )
            ax.add_patch(plt.Circle((0, 0), 0.55, fc="#FAFAFA"))
            ax.set_title("Framing Share (Donut)")
            for at in autotexts:
                at.set_fontsize(9)
            plt.tight_layout()
            st.pyplot(fig)

    elif framing_view == "Per-Crisis Stacked Bar":
        if "crisis_name" not in framing_df.columns:
            st.error("`crisis_name` not found in framing CSV.")
        else:
            pivot = (framing_df.groupby(["crisis_name", framing_type_col])[framing_count_col]
                     .sum().unstack(fill_value=0))
            pivot_norm = pivot.div(pivot.sum(axis=1), axis=0) * 100
            fig, ax = plt.subplots(figsize=(10, 5))
            bottom = np.zeros(len(pivot_norm))
            for j, c in enumerate(pivot_norm.columns):
                vals = pivot_norm[c].values
                ax.bar(pivot_norm.index, vals, bottom=bottom,
                       color=FRAME_COLORS[j % len(FRAME_COLORS)],
                       label=c, edgecolor="white", linewidth=0.4)
                for i, (v, b) in enumerate(zip(vals, bottom)):
                    if v > 7:
                        ax.text(i, b+v/2, f"{v:.0f}%", ha="center", va="center",
                                fontsize=9, color="white", fontweight="bold")
                bottom += vals
            ax.set_title("Narrative Framing per Crisis (100% stacked)")
            ax.set_ylabel("Share of Articles (%)")
            ax.set_ylim(0, 105)
            plt.xticks(rotation=30, ha="right")
            ax.legend(loc="upper right", fontsize=9)
            plt.tight_layout()
            st.pyplot(fig)

    else:  # Framing vs Coverage scatter
        if "crisis_name" not in framing_df.columns or "raw_coverage" not in crises_df.columns:
            st.error("Missing `crisis_name` in framing CSV or `raw_coverage` in crises CSV.")
        else:
            fr_pivot = (framing_df.groupby(["crisis_name", framing_type_col])[framing_count_col]
                        .sum().unstack(fill_value=0))
            fr_pivot = fr_pivot.div(fr_pivot.sum(axis=1), axis=0)
            fr_pivot = fr_pivot.merge(
                crises_df.set_index("crisis_name")[["raw_coverage"]],
                left_index=True, right_index=True
            )
            framing_types = [c for c in fr_pivot.columns if c != "raw_coverage"]
            ncols = 3
            nrows = -(-len(framing_types) // ncols)
            fig, axes = plt.subplots(nrows, ncols, figsize=(13, 4.5*nrows))
            axes = np.array(axes).flatten()
            for idx, ftype in enumerate(framing_types):
                ax = axes[idx]
                x = fr_pivot[ftype].values
                y = fr_pivot["raw_coverage"].values
                ax.scatter(x, y, s=80, color=FRAME_COLORS[idx % len(FRAME_COLORS)],
                           edgecolors="white", linewidths=1)
                for cname, xi, yi in zip(fr_pivot.index, x, y):
                    ax.annotate(cname, (xi, yi), xytext=(5, 3),
                                textcoords="offset points", fontsize=7.5)
                if len(x) > 1:
                    m_c, b_c = np.polyfit(x, y, 1)
                    xl = np.linspace(x.min(), x.max(), 100)
                    ax.plot(xl, m_c*xl+b_c, "--", color="#999", linewidth=1.2)
                    r2_f = r2_score(y, m_c*x+b_c) if len(set(x)) > 1 else 0
                    ax.set_title(f"{ftype.capitalize()}\n(R²={r2_f:.3f})", fontsize=11)
                else:
                    ax.set_title(ftype.capitalize(), fontsize=11)
                ax.set_xlabel("Framing ratio")
                ax.set_ylabel("Raw coverage")
            for j in range(len(framing_types), len(axes)):
                axes[j].set_visible(False)
            plt.suptitle("Framing Ratio vs Raw Coverage per Crisis",
                         fontsize=13, fontweight="bold", y=1.01)
            plt.tight_layout()
            st.pyplot(fig)

    st.divider()
    st.markdown("**Entity Sentiment**")
    if not sentiment_df.empty:
        sent_entity_col = "entity_name" if "entity_name" in sentiment_df.columns else sentiment_df.columns[0]
        sent_score_col  = "sentiment_score" if "sentiment_score" in sentiment_df.columns else sentiment_df.select_dtypes("number").columns[0]

        ent = sentiment_df.groupby(sent_entity_col)[sent_score_col].mean().sort_values()
        fig, ax = plt.subplots(figsize=(8, 4))
        colors_s = [SENT_PAL["negative"] if v < 0 else SENT_PAL["positive"] for v in ent.values]
        ax.barh(ent.index, ent.values, color=colors_s, edgecolor="white")
        ax.axvline(0, color="#333", linewidth=0.8)
        ax.set_title("Average Entity Sentiment Score")
        ax.set_xlabel("Sentiment Score  (negative = left, positive = right)")
        plt.tight_layout()
        st.pyplot(fig)
        st.info(
            "**Insight:** Western-aligned actors (Zelensky) are the only net-positive figures; "
            "opposing actors (Hamas, Putin) are overwhelmingly negative — a structural feature "
            "of the outlets in this dataset."
        )

# ═══════════════════════════════════════════════════════════════════════════════
# 6 · Model Results
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "6 · Model Results":
    st.subheader("Predictive Modelling — What drives monthly coverage?")

    if model_df.empty:
        st.error("monthly_model_data.csv could not be loaded.")
        st.stop()

    # Use the same features as the notebook
    candidate_features = [
        "fund_required", "crisis_days", "people_affected",
        "is_onset", "top3_outlet_ratio", "months_since_start",
        "framing_ratio_humanitarian", "framing_ratio_geopolitical",
        "framing_ratio_economic", "post_onset_ratio", "outlet_hhi", "onset"
    ]
    target_col = "log_coverage" if "log_coverage" in model_df.columns else "coverage_count"
    available  = [f for f in candidate_features if f in model_df.columns]

    if not available:
        st.error(f"No feature columns found. Columns in model CSV: {list(model_df.columns)}")
        st.stop()
    if target_col not in model_df.columns:
        st.error(f"`{target_col}` not found in model CSV.")
        st.stop()

    clean_df = model_df[available + [target_col]].dropna()
    X = clean_df[available].values
    y = clean_df[target_col].values

    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    X_tr, X_te, y_tr, y_te = train_test_split(X_s, y, test_size=0.2, random_state=42)

    models = {
        "Linear Regression":  LinearRegression(),
        "Ridge Regression":   Ridge(alpha=1.0),
        "Decision Tree":      DecisionTreeRegressor(max_depth=5, random_state=42),
        "Random Forest":      RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    }

    results, fitted, preds_dict = [], {}, {}
    for name, m in models.items():
        m.fit(X_tr, y_tr)
        pred = m.predict(X_te)
        preds_dict[name] = pred
        results.append({
            "Model": name,
            "R²":    round(r2_score(y_te, pred), 3),
            "RMSE":  round(mean_squared_error(y_te, pred)**0.5, 3),
            "MAE":   round(mean_absolute_error(y_te, pred), 3),
        })
        fitted[name] = m
    results_df = pd.DataFrame(results)

    # ── Panel toggle ──────────────────────────────────────────────────────────
    panel = st.radio("Panel", [
        "Model Comparison", "Feature Importance", "Actual vs Predicted", "Residual Analysis"
    ], horizontal=True)

    if panel == "Model Comparison":
        c1, c2 = st.columns([1.2, 1])
        with c1:
            st.dataframe(
                results_df.style
                  .highlight_max(subset=["R²"],         color="#d4edda")
                  .highlight_min(subset=["RMSE","MAE"], color="#d4edda"),
                use_container_width=True
            )
        with c2:
            fig, axes = plt.subplots(1, 3, figsize=(12, 4))
            palette = ["#2A9D8F","#457B9D","#E9C46A","#F4A261"]
            for ax, metric in zip(axes, ["R²","RMSE","MAE"]):
                bars = ax.bar(results_df["Model"], results_df[metric],
                              color=palette, edgecolor="white", width=0.55)
                for bar, val in zip(bars, results_df[metric]):
                    ax.text(bar.get_x()+bar.get_width()/2,
                            bar.get_height()+results_df[metric].max()*0.02,
                            f"{val:.3f}", ha="center", fontsize=9)
                ax.set_title(metric, fontsize=12)
                ax.tick_params(axis="x", rotation=20, labelsize=8)
            plt.suptitle("Model Performance Comparison", fontsize=13, fontweight="bold")
            plt.tight_layout()
            st.pyplot(fig)

    elif panel == "Feature Importance":
        lr_model = fitted["Linear Regression"]
        rf_model = fitted["Random Forest"]
        fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

        coef_df = pd.DataFrame({
            "Feature": available, "Coefficient": lr_model.coef_
        }).sort_values("Coefficient", ascending=True)
        colors_c = [SENT_PAL["negative"] if v < 0 else SENT_PAL["positive"]
                    for v in coef_df["Coefficient"]]
        axes[0].barh(coef_df["Feature"], coef_df["Coefficient"],
                     color=colors_c, edgecolor="white", height=0.6)
        axes[0].axvline(0, color="#333", linewidth=0.8)
        axes[0].set_title("Linear Regression — Coefficients\n(green = increases coverage, red = decreases)",
                          fontsize=11)

        imp_df = pd.DataFrame({
            "Feature": available, "Importance": rf_model.feature_importances_
        }).sort_values("Importance", ascending=True)
        axes[1].barh(imp_df["Feature"], imp_df["Importance"],
                     color="#457B9D", edgecolor="white", height=0.6)
        axes[1].set_title("Random Forest — Feature Importance\n(mean decrease in impurity)",
                          fontsize=11)

        plt.suptitle("What Drives Monthly Media Coverage?", fontsize=13, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)

    elif panel == "Actual vs Predicted":
        palette = ["#2A9D8F","#457B9D","#E9C46A","#F4A261"]
        fig, axes = plt.subplots(1, 4, figsize=(18, 4.5))
        for ax, (name, yp), color in zip(axes, preds_dict.items(), palette):
            ax.scatter(y_te, yp, alpha=0.45, s=18, color=color,
                       edgecolors="white", linewidths=0.3)
            mn = min(y_te.min(), yp.min()) * 0.95
            mx = max(y_te.max(), yp.max()) * 1.05
            ax.plot([mn,mx],[mn,mx],"--",color="#999",linewidth=1.2)
            ax.set_title(f"{name}\nR²={r2_score(y_te,yp):.3f}", fontsize=9, fontweight="bold")
            ax.set_xlabel("Actual log coverage")
            ax.set_ylabel("Predicted")
        plt.suptitle("Actual vs Predicted — All Models", fontsize=13, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)

    else:  # Residual Analysis
        best_name  = results_df.sort_values("R²", ascending=False).iloc[0]["Model"]
        best_preds = preds_dict[best_name]
        residuals  = y_te - best_preds
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
        axes[0].scatter(best_preds, residuals, alpha=0.45, s=18,
                        color="#457B9D", edgecolors="white", linewidths=0.3)
        axes[0].axhline(0, color="#E63946", linestyle="--", linewidth=1.5)
        axes[0].set_xlabel("Predicted log coverage")
        axes[0].set_ylabel("Residual")
        axes[0].set_title("Residuals vs Fitted")
        axes[1].hist(residuals, bins=30, color="#2A9D8F", edgecolor="white")
        axes[1].set_xlabel("Residual")
        axes[1].set_ylabel("Count")
        axes[1].set_title("Residual Distribution")
        plt.suptitle(f"Residual Analysis — {best_name}", fontsize=13, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)

    st.info(
        "**Key finding:** Coverage is driven more by framing and timing (onset period) than by "
        "raw humanitarian severity. Larger funding requirements → more coverage; "
        "longer-running crises → less per month."
    )