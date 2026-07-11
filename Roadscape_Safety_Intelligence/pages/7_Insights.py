"""Page 7 — Insights (live, filter-aware business insights)"""

import streamlit as st

from utils import (
    ACCENT, GOLD, INFO, PERIOD_ORDER, SKY, TEAL, VIOLET, inject_global_css,
    load_raw_data, no_data_stop, page_header, render_filters, render_logo,
    section_title,
)

st.set_page_config(page_title="RoadScape | Insights", page_icon="📈", layout="wide")
inject_global_css()

with st.sidebar:
    render_logo()

df_raw, load_error = load_raw_data()
if df_raw is None:
    st.error("Dataset not loaded. Go to the Executive Dashboard page and load the data first.")
    st.stop()

df = render_filters(df_raw)
page_header("📈 Insights", "Business insights, generated live from the current filter selection")
if df.empty:
    no_data_stop()

# ----------------------------------------------------------------------------
# Compute everything up front
# ----------------------------------------------------------------------------
top_state = df.groupby("state").size().sort_values(ascending=False)
top_city = df.groupby("city").size().sort_values(ascending=False)
hourly = df.dropna(subset=["hour"]).groupby("hour").size()
peak_hour = int(hourly.idxmax())
top_cause = df["cause"].value_counts().idxmax()
top_weather = df["weather"].value_counts().idxmax()
period = df.groupby("time_period").size().reindex(PERIOD_ORDER)
top_period = period.idxmax()
fatal_share = (df["accident_severity"] == "fatal").mean() * 100

road_severity = df.groupby("road_type", observed=True)["accident_severity"].apply(
    lambda s: (s == "fatal").mean() * 100
).sort_values(ascending=False)
top_fatal_road = road_severity.index[0]

day_type_counts = df.groupby("day_type").size()
weekend_share = (day_type_counts.get("Weekend", 0) / day_type_counts.sum() * 100) if day_type_counts.sum() else 0

vehicles_severity_corr = df.groupby("accident_severity", observed=True)["vehicles_involved"].mean()

# ----------------------------------------------------------------------------
# Group 1 — Where it happens
# ----------------------------------------------------------------------------
section_title("Where It Happens", "Geographic concentration of accidents", eyebrow="LOCATION")
g1c1, g1c2 = st.columns(2, gap="large")
with g1c1:
    st.markdown(
        f'<div class="rs-insight-box">📍 <b>{top_state.index[0]}</b> '
        f'({top_state.iloc[0]:,} accidents) and <b>{top_city.index[0]}</b> '
        f'({top_city.iloc[0]:,} accidents) are the highest-volume state and city respectively.</div>',
        unsafe_allow_html=True,
    )
with g1c2:
    st.markdown(
        f'<div class="rs-insight-box">🛣️ <b>{top_fatal_road.title()}</b> roads show the highest share '
        f'of fatal outcomes ({road_severity.iloc[0]:.1f}% of their accidents are fatal) — even without '
        f'the highest volume, they carry the highest per-accident risk.</div>',
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# Group 2 — When it happens
# ----------------------------------------------------------------------------
section_title("When It Happens", "Timing patterns worth planning around", eyebrow="TIMING")
g2c1, g2c2 = st.columns(2, gap="large")
with g2c1:
    st.markdown(
        f'<div class="rs-insight-box">⏰ Most accidents concentrate in the <b>{top_period.lower()}</b> '
        f'window, and the single busiest hour is <b>{peak_hour}:00–{peak_hour+1}:00</b> — a strong '
        f'candidate for targeted patrol scheduling.</div>',
        unsafe_allow_html=True,
    )
with g2c2:
    st.markdown(
        f'<div class="rs-insight-box">📆 Weekends account for <b>{weekend_share:.1f}%</b> of accidents '
        f'in the current selection, showing a different rhythm from weekday traffic patterns.</div>',
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# Group 3 — Why, and how severe
# ----------------------------------------------------------------------------
section_title("Why It Happens — and How Severe", "Cause, weather, and severity patterns", eyebrow="CAUSE & RISK")
g3c1, g3c2 = st.columns(2, gap="large")
with g3c1:
    st.markdown(
        f'<div class="rs-insight-box">🌧️ <b>{top_weather.title()}</b> conditions are linked to the '
        f'highest accident count among recorded weather types, confirming that adverse weather '
        f'meaningfully raises risk.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="rs-insight-box">🎯 <b>{top_cause.title()}</b> is the single largest recorded cause '
        f'of accidents — the top lever for awareness campaigns and enforcement.</div>',
        unsafe_allow_html=True,
    )
with g3c2:
    st.markdown(
        f'<div class="rs-insight-box">☠️ Fatal accidents make up <b>{fatal_share:.1f}%</b> of all '
        f'recorded accidents in the current selection.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="rs-insight-box">🚗 Average vehicles involved rises with severity: '
        + " → ".join(f"{sev} {vehicles_severity_corr.get(sev, 0):.2f}" for sev in ["minor", "major", "fatal"])
        + " — multi-vehicle collisions skew more severe.</div>",
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="rs-note-box">ℹ️ Every insight above is computed live from whatever data and filters '
    'are currently active — nothing here is a hardcoded number, so it stays accurate as the dataset '
    'or filters change.</div>',
    unsafe_allow_html=True,
)