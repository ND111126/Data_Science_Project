"""Page 10 — Analytics Workflow

Documents how RoadScape actually got built: the end-to-end analytics
pipeline, the tools used, and a summary of what each underlying Jupyter
notebook covers. This page is descriptive (about the project itself),
so it doesn't filter by the sidebar selections the way the analytical
pages do — it always reflects the full project.

Note: if your project already has an "About & Methodology" page numbered
9, just rename this file to 10_Analytics_Workflow.py (or whatever slot is
next) so the sidebar order doesn't collide.
"""

import streamlit as st

from utils import (
    ACCENT, CARD, CARD_BORDER, GOLD, MUTED, SKY, TEAL, TEXT, VIOLET,
    inject_global_css, load_raw_data, page_header, render_filters,
    render_logo, section_title,
)

st.set_page_config(page_title="RoadScape | Analytics Workflow", page_icon="🧭", layout="wide")
inject_global_css()

with st.sidebar:
    render_logo()

df_raw, load_error = load_raw_data()
if df_raw is None:
    st.error("Dataset not loaded. Go to the Executive Dashboard page and load the data first.")
    st.stop()

# Keep the sidebar filter UI consistent across pages, even though this
# page's content doesn't depend on the filtered selection.
_ = render_filters(df_raw)

page_header("🧭 Analytics Workflow", "How raw accident records became the RoadScape dashboard")

# =============================================================================
# Local styling for the workflow flow-chart (scoped to this page)
# =============================================================================
st.markdown(
    f"""
    <style>
        .rs-phase {{
            margin-top: 18px;
            margin-bottom: 22px;
        }}
        .rs-phase-label {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
        }}
        .rs-phase-tag {{
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 1px;
            text-transform: uppercase;
            padding: 3px 11px;
            border-radius: 20px;
            color: #0B0E14;
        }}
        .rs-phase-title {{
            font-size: 1rem;
            font-weight: 700;
            color: {TEXT};
        }}
        .rs-wf-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
        }}
        .rs-wf-card {{
            flex: 1 1 240px;
            background: {CARD};
            border: 1px solid {CARD_BORDER};
            border-top: 3px solid var(--wf-accent, {ACCENT});
            border-radius: 12px;
            padding: 16px 18px;
            min-width: 220px;
        }}
        .rs-wf-card .rs-wf-top {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }}
        .rs-wf-num {{
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background: var(--wf-accent, {ACCENT});
            color: #0B0E14;
            font-weight: 800;
            font-size: 0.78rem;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .rs-wf-icon {{ font-size: 1.15rem; }}
        .rs-wf-card h4 {{
            margin: 0;
            font-size: 0.92rem;
            font-weight: 700;
            color: {TEXT};
        }}
        .rs-wf-card p {{
            margin: 0;
            font-size: 0.8rem;
            color: {MUTED};
            line-height: 1.5;
        }}
        .rs-tech-row {{
            display: flex;
            justify-content: space-between;
            background: {CARD};
            border: 1px solid {CARD_BORDER};
            border-left: 3px solid {ACCENT};
            border-radius: 8px;
            padding: 8px 14px;
            margin-bottom: 6px;
            font-size: 0.86rem;
            color: {TEXT};
        }}
        .rs-tech-row b {{ color: {ACCENT}; min-width: 130px; display: inline-block; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# PROJECT WORKFLOW
# =============================================================================
section_title("Project Workflow", "The end-to-end pipeline, from problem statement to dashboard",
              eyebrow="PIPELINE")

phases = [
    {
        "tag": "PHASE 1 · FOUNDATION", "accent": TEAL,
        "steps": [
            ("🧩", "Business Understanding",
             "Defined the problem statement, objectives, and 5 business-question categories."),
            ("📋", "Dataset Understanding",
             "Audited structure, types, and quality across 20,000 records and 16 fields."),
            ("🧹", "Data Cleaning & Validation",
             "Confirmed zero missing values and zero duplicates — no treatment needed."),
        ],
    },
    {
        "tag": "PHASE 2 · ANALYSIS", "accent": VIOLET,
        "steps": [
            ("🔎", "Exploratory Data Analysis",
             "Explored location, time, and environmental patterns across three notebooks."),
            ("🔗", "Relationship Analysis",
             "Cross-tabulated conditions against severity to surface hidden patterns."),
            ("⚖️", "Risk & Safety Scoring",
             "Combined six weighted indicators into one Composite Risk Score per state."),
        ],
    },
    {
        "tag": "PHASE 3 · SYNTHESIS", "accent": GOLD,
        "steps": [
            ("💡", "Business Insights",
             "Translated statistical patterns into plain-language, decision-ready findings."),
            ("✅", "Recommendations",
             "Converted insights into concrete, actionable road-safety measures."),
        ],
    },
    {
        "tag": "PHASE 4 · DELIVERY", "accent": SKY,
        "steps": [
            ("📊", "Interactive Dashboard",
             "Rebuilt every finding as a live, filter-aware multipage Streamlit app."),
            ("📁", "Documentation & GitHub",
             "Packaged the project with a README, methodology notes, and version control."),
        ],
    },
]

for phase in phases:
    st.markdown(
        f'<div class="rs-phase">'
        f'<div class="rs-phase-label">'
        f'<span class="rs-phase-tag" style="background:{phase["accent"]};">{phase["tag"]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    row_html = f'<div class="rs-wf-row" style="--wf-accent:{phase["accent"]};">'
    for i, (icon, title, desc) in enumerate(phase["steps"], start=1):
        row_html += (
            f'<div class="rs-wf-card">'
            f'<div class="rs-wf-top">'
            f'<div class="rs-wf-num">{i}</div>'
            f'<span class="rs-wf-icon">{icon}</span>'
            f'<h4>{title}</h4>'
            f'</div>'
            f'<p>{desc}</p>'
            f'</div>'
        )
    row_html += "</div></div>"
    st.markdown(row_html, unsafe_allow_html=True)

st.markdown(
    '<div class="rs-note-box">ℹ️ Every stage above happened in its own notebook (except the final '
    'two) before any dashboard code was written — the dashboard is the last stage of the pipeline, '
    'not the starting point.</div>',
    unsafe_allow_html=True,
)

# =============================================================================
# TECHNOLOGY STACK
# =============================================================================
section_title("Technology Stack", "Tools used at each stage of the project", eyebrow="STACK")

tech = [
    ("Python", "Core language for analysis and dashboard development."),
    ("Pandas", "Data loading, cleaning, transformation, and aggregation."),
    ("NumPy", "Numerical computation and array operations."),
    ("Matplotlib", "Static exploratory visualizations in the notebooks."),
    ("Seaborn", "Statistical plots and relationship/heatmap analysis."),
    ("Plotly", "Interactive charts and the accident hotspot map."),
    ("Streamlit", "The interactive multipage RoadScape dashboard."),
    ("Jupyter Notebook", "Analysis, documentation, and business-question tracking."),
    ("Git & GitHub", "Version control and project presentation."),
]
tc1, tc2 = st.columns(2, gap="large")
for i, (name, purpose) in enumerate(tech):
    target = tc1 if i % 2 == 0 else tc2
    with target:
        st.markdown(
            f'<div class="rs-tech-row"><b>{name}</b>{purpose}</div>',
            unsafe_allow_html=True,
        )

# =============================================================================
# NOTEBOOK SUMMARIES
# =============================================================================
section_title("Notebook Summaries", "What each underlying analysis notebook actually covers",
              eyebrow="NOTEBOOKS")

with st.expander("🧩 Business Understanding — framing the problem"):
    st.markdown(
        "Sets up the whole project before any data is touched: the problem statement, 7 project "
        "objectives, and 5 business-question categories (where accidents happen, when, under what "
        "conditions, how severe, and what to recommend). Also lays out the 10-stage project workflow "
        "and the technology stack used throughout. This notebook doesn't analyze data itself — it's "
        "the roadmap the other six notebooks follow."
    )

with st.expander("📋 Dataset Understanding — first look at the raw data"):
    st.markdown(
        "First pass over the raw dataset: shape (20,000 rows × 16 columns), column list, dtypes, "
        "`describe()` for both numeric and categorical columns, missing-value check (none found), "
        "and duplicate-record check (none found). Confirms the data spans **January 2022 – April "
        "2025**, with an average of about 3 vehicles and 2 casualties per accident, and concludes the "
        "dataset is clean and ready for EDA without further treatment."
    )

with st.expander("📍 Location Intelligence — where accidents concentrate"):
    st.markdown(
        "Geographic EDA: accidents by state (Maharashtra highest, followed by Punjab and Tamil Nadu), "
        "the concentration among the top 5 states, the top 10 accident-prone cities, average "
        "casualties per accident by state, a vehicles-involved-vs-casualties scatter plot, the overall "
        "casualty-count distribution, and a latitude/longitude hotspot map. This is the direct basis "
        "for the dashboard's Location Intelligence page and the Overview's Geographic Analysis section."
    )

with st.expander("⏰ Time Intelligence — when accidents happen"):
    st.markdown(
        "Temporal EDA across four dimensions: year-over-year trend, monthly seasonality, day-of-week "
        "pattern, and hour-of-day pattern, plus a time-period (Morning/Afternoon/Evening/Night) share. "
        "Feeds the dashboard's Time Intelligence page directly."
    )
    st.markdown(
        '<div class="rs-note-box">ℹ️ Note: this notebook\'s hourly write-up was checked during the '
        'dashboard build — the dashboard\'s Time Intelligence page computes the peak hour live from '
        'whichever hour has the actual highest count, rather than assuming it based on typical commute '
        'hours, so it stays accurate as filters change.</div>',
        unsafe_allow_html=True,
    )

with st.expander("🌦️ Environmental & Severity Intelligence — conditions behind accidents"):
    st.markdown(
        "Examines weather, road type, traffic density, traffic signal presence, and accident cause as "
        "drivers of accident frequency and severity — including a traffic-density-vs-casualties boxplot "
        "and a traffic-signal-vs-severity heatmap. Directly informs the dashboard's Weather & Road "
        "Conditions page."
    )

with st.expander("🔗 Relationship Analysis — cross-factor patterns"):
    st.markdown(
        "Goes deeper than single-variable EDA: cross-tabulates traffic density, visibility, weather, "
        "road type, cause, and traffic-signal presence against accident severity and casualties, using "
        "heatmaps to surface combinations that standard bar charts miss. This is the basis for several "
        "of the dashboard's severity cross-tab visuals, like the Weather × Severity heatmap."
    )

with st.expander("⚖️ Composite Risk Intelligence — scoring and ranking states"):
    st.markdown(
        "Builds the Composite RoadScape Risk Score by normalizing six indicators onto a 0–100 scale — "
        "accident frequency (30%), average casualties (25%), severe accidents (20%), high traffic "
        "density (10%), poor visibility (10%), and bad weather (5%) — then ranks states, classifies "
        "them into Low/Medium/High risk, and generates a recommendation per tier. Maharashtra ranks "
        "highest."
    )
    st.markdown(
        '<div class="rs-note-box">ℹ️ Note: this notebook assigns tiers using a fixed rank cutoff '
        '(top 2 states = High, next 3 = Medium, rest = Low). The dashboard\'s risk table instead uses '
        'quantile-based tiering, so the cutoffs adjust automatically as filters change how many states '
        'are in view.</div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr class="rs-divider">', unsafe_allow_html=True)
st.caption("RoadScape — Road Safety Intelligence Platform · O7 Services Data Analytics Internship Project")