"""Page 8 — Recommendations"""

import streamlit as st

from utils import (
    compute_risk_table, inject_global_css, load_raw_data, no_data_stop,
    page_header, render_filters, render_logo, section_title,
)

st.set_page_config(page_title="RoadScape | Recommendations", page_icon="🎯", layout="wide")
inject_global_css()

with st.sidebar:
    render_logo()

df_raw, load_error = load_raw_data()
if df_raw is None:
    st.error("Dataset not loaded. Go to the Executive Dashboard page and load the data first.")
    st.stop()

df = render_filters(df_raw)
page_header("🎯 Recommendations", "Turning the data into concrete road-safety actions")
if df.empty:
    no_data_stop()

hourly = df.dropna(subset=["hour"]).groupby("hour").size()
peak_hour = int(hourly.idxmax())
top_cause = df["cause"].value_counts().idxmax()
risk_df = compute_risk_table(df)
high_risk_states = risk_df.loc[risk_df["Risk_Level"] == "High", "state"].tolist() if not risk_df.empty else []

# ----------------------------------------------------------------------------
section_title(
    "Composite RoadScape Risk Score",
    "30% Accident Frequency · 25% Avg. Casualties · 20% Severe Accidents · "
    "10% High Traffic · 10% Poor Visibility · 5% Bad Weather",
    eyebrow="RISK RANKING",
)
if not risk_df.empty:
    def highlight_risk(row):
        color = {"High": "background-color:#FF3B4E; color:white;",
                 "Medium": "background-color:#F5A623; color:black;",
                 "Low": "background-color:#22C55E; color:white;"}[str(row["Risk_Level"])]
        return [color if col == "Risk_Level" else "" for col in row.index]

    display_cols = ["Rank", "state", "Total_Accidents", "Avg_Casualties",
                     "Severe_Accidents", "Composite_Risk_Score", "Risk_Level", "Recommendation"]
    styled = risk_df[display_cols].style.apply(highlight_risk, axis=1).format(
        {"Avg_Casualties": "{:.2f}", "Composite_Risk_Score": "{:.2f}"}
    )
    st.dataframe(styled, use_container_width=True, height=290)
else:
    st.info("Not enough state-level data in the current filter selection to compute a risk score.")

# ----------------------------------------------------------------------------
section_title("Enforcement & Infrastructure", "Where to put cameras, signage, and signals",
              eyebrow="ACT NOW")
e1, e2 = st.columns(2, gap="large")
with e1:
    st.markdown(
        f'<div class="rs-recommend-box">✅ <b>Install speed cameras and increase enforcement</b> at '
        f'hotspots in {", ".join(high_risk_states) if high_risk_states else "the top-ranked states above"}, '
        f'where the Composite Risk Score is highest.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="rs-recommend-box">✅ <b>Add warning signage and speed-calming measures</b> in '
        'accident-prone zones flagged by the hotspot map on the Location Intelligence page.</div>',
        unsafe_allow_html=True,
    )
with e2:
    st.markdown(
        '<div class="rs-recommend-box">✅ <b>Improve street lighting</b> on roads with a high share of '
        'low-visibility accidents, particularly outside urban cores.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="rs-recommend-box">✅ <b>Strengthen traffic-signal coverage and maintenance</b> at '
        'intersections showing elevated severe-accident rates.</div>',
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
section_title("Response & Awareness", "Reducing harm once an accident happens, and preventing the next one",
              eyebrow="BUILD OVER TIME")
r1, r2 = st.columns(2, gap="large")
with r1:
    st.markdown(
        f'<div class="rs-recommend-box">✅ <b>Increase patrols during high-risk hours</b>, especially '
        f'around <b>{peak_hour}:00–{peak_hour+2}:00</b>, when accident frequency peaks.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="rs-recommend-box">✅ <b>Prioritize faster emergency-response protocols</b> in '
        'high-casualty states/cities to reduce fatality outcomes once an accident occurs.</div>',
        unsafe_allow_html=True,
    )
with r2:
    st.markdown(
        f'<div class="rs-recommend-box">✅ <b>Run targeted awareness campaigns</b> addressing '
        f'<b>{top_cause}</b>, the leading recorded cause of accidents — the single highest-leverage '
        f'behavioral intervention.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="rs-recommend-box">✅ <b>Launch driver-awareness campaigns for young / new '
        'drivers</b>, focusing on the leading accident causes and highest-risk time windows identified '
        'in this dashboard.</div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr class="rs-divider">', unsafe_allow_html=True)
st.caption("RoadScape — Road Safety Intelligence Platform · O7 Services Data Analytics Internship Project")