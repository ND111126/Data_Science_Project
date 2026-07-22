"""Page 6 — Time Intelligence"""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import (
    CHART_H, DAY_ORDER, MONTH_ORDER, PERIOD_ORDER, PLOTLY_TEMPLATE, PRIMARY,
    generate_time_insights, generate_time_recommendations, inject_global_css,
    load_raw_data, no_data_stop, page_header, render_filters, render_logo,
    render_insight_recommendation_panels, section_title,
)

st.set_page_config(page_title="RoadScape | Time Intelligence", page_icon="⏰", layout="wide")
inject_global_css()

with st.sidebar:
    render_logo()

df_raw, load_error = load_raw_data()
if df_raw is None:
    st.error("Dataset not loaded. Go to the Executive Dashboard page and load the data first.")
    st.stop()

df = render_filters(df_raw)
page_header("⏰ Time Intelligence", "When do accidents happen — and when should patrols focus?")
if df.empty:
    no_data_stop()

c1, c2 = st.columns([1.4, 1], gap="large")
with c1:
    section_title("Hourly Accident Pattern (0–23h)")
    hourly = df.dropna(subset=["hour"]).groupby("hour").size().reset_index(name="Accidents")
    peak_hour = int(hourly.loc[hourly["Accidents"].idxmax(), "hour"])
    fig = px.line(hourly, x="hour", y="Accidents", markers=True,
                  color_discrete_sequence=[PRIMARY], template=PLOTLY_TEMPLATE)
    fig.add_vline(x=peak_hour, line_dash="dash", line_color="#F5A623",
                  annotation_text=f"Peak: {peak_hour}:00", annotation_position="top")
    fig.update_xaxes(dtick=1)
    fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    section_title("Weekend vs. Weekday")
    dt = df.groupby("day_type").size().reset_index(name="Accidents")
    fig = px.pie(dt, names="day_type", values="Accidents", hole=0.55,
                 color="day_type", color_discrete_map={"Weekday": "#3B9CFF", "Weekend": PRIMARY},
                 template=PLOTLY_TEMPLATE)
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), showlegend=False,
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2, gap="large")
with c3:
    section_title("Accidents by Day of Week")
    weekday = df.groupby("day_of_week").size().reindex(DAY_ORDER).reset_index(name="Accidents")
    fig = px.bar(weekday, x="day_of_week", y="Accidents", text="Accidents",
                 color="Accidents", color_continuous_scale="Blues", template=PLOTLY_TEMPLATE)
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, coloraxis_showscale=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    section_title("Monthly (Seasonal) Pattern")
    monthly = df.groupby("month").size().reindex(MONTH_ORDER).reset_index(name="Accidents")
    fig = px.bar(monthly, x="month", y="Accidents", color="Accidents",
                 color_continuous_scale="Reds", template=PLOTLY_TEMPLATE)
    fig.update_layout(height=CHART_H, coloraxis_showscale=False, margin=dict(t=10, b=10),
                       xaxis_tickangle=-35, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

section_title("Accidents by Time Period")
period = df.groupby("time_period").size().reindex(PERIOD_ORDER).reset_index(name="Accidents")
fig = px.bar(period, x="time_period", y="Accidents", text="Accidents",
             color="time_period", template=PLOTLY_TEMPLATE,
             color_discrete_map={"Morning": "#FDBE85", "Afternoon": "#F5A623",
                                 "Evening": PRIMARY, "Night": "#1B2A4A"})
fig.update_traces(textposition="outside")
fig.update_layout(height=CHART_H, showlegend=False, margin=dict(t=10, b=10),
                   paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

section_title("Hour × Day-of-Week Heatmap")
heat = (
    df.dropna(subset=["hour"])
    .groupby(["day_of_week", "hour"]).size()
    .reset_index(name="Accidents")
    .pivot(index="day_of_week", columns="hour", values="Accidents")
    .reindex(DAY_ORDER)
    .fillna(0)
)
fig = px.imshow(heat, color_continuous_scale="Reds", aspect="auto", template=PLOTLY_TEMPLATE,
                 labels=dict(x="Hour of Day", y="Day of Week", color="Accidents"))
fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

is_partial = df[df["year"] == df["year"].max()]["date"].dt.dayofyear.max() < 350
if is_partial:
    st.markdown(
        f'<div class="rs-note-box">⚠️ {int(df["year"].max())} data is a partial year in this dataset — '
        f'keep that in mind when comparing it to full calendar years.</div>',
        unsafe_allow_html=True,
    )

st.write("")
render_insight_recommendation_panels(
    generate_time_insights(df), generate_time_recommendations(df),
    insight_caption="Peak hours, days, and weekend vs. weekday patterns.",
    rec_caption="Scheduling-focused safety actions.",
)