"""Page 3 — Weather & Road Conditions"""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import (
    CHART_H, PLOTLY_TEMPLATE, PRIMARY, SEVERITY_COLORS, SEVERITY_ORDER,
    generate_weather_insights, generate_weather_recommendations, inject_global_css,
    load_raw_data, no_data_stop, page_header, render_filters, render_logo,
    render_insight_recommendation_panels, section_title,
)

st.set_page_config(page_title="RoadScape | Weather & Road Conditions", page_icon="🌦️", layout="wide")
inject_global_css()

with st.sidebar:
    render_logo()

df_raw, load_error = load_raw_data()
if df_raw is None:
    st.error("Dataset not loaded. Go to the Executive Dashboard page and load the data first.")
    st.stop()

df = render_filters(df_raw)
page_header("🌦️ Weather & Road Conditions", "Which conditions make accidents more likely — and more severe?")
if df.empty:
    no_data_stop()

c1, c2 = st.columns(2, gap="large")
with c1:
    section_title("Weather — Accident Share")
    w = df.groupby("weather").size().sort_values(ascending=False).reset_index(name="Accidents")
    fig = px.pie(w, names="weather", values="Accidents", hole=0.5,
                 color_discrete_sequence=px.colors.sequential.Blues_r, template=PLOTLY_TEMPLATE)
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), showlegend=False,
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    most_dangerous_weather = w.iloc[0]["weather"]

with c2:
    section_title("Road Type — Accident Volume", "road_type is the closest available field to 'road surface'")
    r = df.groupby("road_type").size().sort_values(ascending=False).reset_index(name="Accidents")
    fig = px.bar(r, x="road_type", y="Accidents", text="Accidents", color="Accidents",
                 color_continuous_scale="Purples", template=PLOTLY_TEMPLATE)
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, coloraxis_showscale=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2, gap="large")
with c3:
    section_title("Day vs Night", "Derived from accident hour (05:00–18:59 = Day, else Night)")
    df["day_night"] = df["hour"].apply(lambda h: "Day" if pd.notna(h) and 5 <= h < 19 else "Night")
    dn = df.groupby("day_night").size().reset_index(name="Accidents")
    fig = px.bar(dn, x="day_night", y="Accidents", text="Accidents",
                 color="day_night", color_discrete_map={"Day": "#F5A623", "Night": "#3B9CFF"},
                 template=PLOTLY_TEMPLATE)
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, showlegend=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    section_title("Visibility Condition", "Used here as the lighting/visibility proxy — the dataset doesn't include a separate 'light condition' field")
    v = df.groupby("visibility").size().sort_values(ascending=False).reset_index(name="Accidents")
    fig = px.bar(v, x="visibility", y="Accidents", text="Accidents", color="Accidents",
                 color_continuous_scale="Oranges", template=PLOTLY_TEMPLATE)
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, coloraxis_showscale=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

section_title("Traffic Signal Presence (Junction Control proxy) vs. Severity")
ts = df.groupby(["traffic_signal_label", "accident_severity"], observed=True).size().reset_index(name="Accidents")
fig = px.bar(ts, x="traffic_signal_label", y="Accidents", color="accident_severity", barmode="group",
             color_discrete_map=SEVERITY_COLORS, template=PLOTLY_TEMPLATE,
             labels={"traffic_signal_label": "Traffic Signal"})
fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

c5, c6 = st.columns(2, gap="large")
with c5:
    section_title("Weather × Severity (row %)")
    cross = pd.crosstab(df["weather"], df["accident_severity"], normalize="index") * 100
    cross = cross.reindex(columns=SEVERITY_ORDER)
    fig = px.imshow(cross.round(1), text_auto=True, color_continuous_scale="Reds",
                     template=PLOTLY_TEMPLATE, labels=dict(x="Severity", y="Weather", color="%"))
    fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c6:
    section_title("Traffic Density — Avg. Casualties")
    td = df.groupby("traffic_density")["casualties"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(td, x="traffic_density", y="casualties", text=td["casualties"].round(2),
                 color="casualties", color_continuous_scale="Reds", template=PLOTLY_TEMPLATE,
                 labels={"casualties": "Avg. Casualties"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, coloraxis_showscale=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    f'<div class="rs-insight-box">🌧️ <b>{most_dangerous_weather.title()}</b> weather is associated with '
    f'the highest number of accidents in the current filter selection.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="rs-note-box">ℹ️ This dataset does not include separate "light condition" or '
    '"junction control" fields, so visibility and traffic-signal presence are used as the closest '
    'available proxies above.</div>',
    unsafe_allow_html=True,
)

st.write("")
render_insight_recommendation_panels(
    generate_weather_insights(df), generate_weather_recommendations(df),
    insight_caption="How weather and visibility relate to fatal outcomes.",
    rec_caption="Environment-focused safety actions.",
)