"""Page 5 — Casualty Analysis

Note: the dataset has no driver-level fields (gender, age, casualty class,
pedestrian flag), so this page focuses on casualty patterns across the
dimensions the data does support — severity, cause, state, road type, and
traffic-signal presence.
"""

import plotly.express as px
import streamlit as st

from utils import (
    CHART_H, PLOTLY_TEMPLATE, PRIMARY, SEVERITY_COLORS, SEVERITY_ORDER,
    generate_casualty_insights, generate_casualty_recommendations, inject_global_css,
    load_raw_data, no_data_stop, page_header, render_filters, render_logo,
    render_insight_recommendation_panels, section_title,
)

st.set_page_config(page_title="RoadScape | Casualty Analysis", page_icon="👥", layout="wide")
inject_global_css()

with st.sidebar:
    render_logo()

df_raw, load_error = load_raw_data()
if df_raw is None:
    st.error("Dataset not loaded. Go to the Executive Dashboard page and load the data first.")
    st.stop()

df = render_filters(df_raw)
page_header("👥 Casualty Analysis", "How severe are the outcomes, and where do they concentrate?")
if df.empty:
    no_data_stop()

st.markdown(
    '<div class="rs-note-box">ℹ️ This dataset doesn\'t include driver-level fields (gender, age, '
    'pedestrian/casualty class) — casualties are recorded as a per-accident count. This page analyzes '
    'casualty patterns across severity, cause, location, and road conditions instead.</div>',
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2, gap="large")
with c1:
    section_title("Casualties — Distribution")
    cas = df["casualties"].value_counts().sort_index().reset_index()
    cas.columns = ["casualties", "count"]
    fig = px.bar(cas, x="casualties", y="count", text="count",
                 color_discrete_sequence=[PRIMARY], template=PLOTLY_TEMPLATE,
                 labels={"count": "Accidents"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    section_title("Casualty Type Share (by Severity)", "Severity used as the available proxy for casualty class")
    sev = df.groupby("accident_severity", observed=True)["casualties"].sum().reindex(SEVERITY_ORDER).reset_index()
    fig = px.pie(sev, names="accident_severity", values="casualties", hole=0.5,
                 color="accident_severity", color_discrete_map=SEVERITY_COLORS, template=PLOTLY_TEMPLATE)
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), showlegend=False,
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2, gap="large")
with c3:
    section_title("Casualties by Accident Cause")
    cc = df.groupby("cause")["casualties"].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(cc, x="casualties", y="cause", orientation="h", text="casualties",
                 color="casualties", color_continuous_scale="Reds", template=PLOTLY_TEMPLATE)
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    section_title("Casualties by Road Type")
    rc = df.groupby("road_type")["casualties"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(rc, x="road_type", y="casualties", text=rc["casualties"].round(2),
                 color="casualties", color_continuous_scale="Oranges", template=PLOTLY_TEMPLATE,
                 labels={"casualties": "Avg. Casualties"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, coloraxis_showscale=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

section_title("Casualties by State")
sc = df.groupby("state")["casualties"].sum().sort_values(ascending=False).reset_index()
fig = px.bar(sc, x="state", y="casualties", text="casualties",
             color="casualties", color_continuous_scale="Reds", template=PLOTLY_TEMPLATE,
             labels={"casualties": "Total Casualties"})
fig.update_traces(textposition="outside")
fig.update_layout(height=CHART_H, coloraxis_showscale=False, margin=dict(t=10, b=10),
                   paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

section_title("Traffic Signal Presence vs. Casualties")
tsc = df.groupby("traffic_signal_label")["casualties"].mean().reset_index()
fig = px.bar(tsc, x="traffic_signal_label", y="casualties", text=tsc["casualties"].round(2),
             color="traffic_signal_label", color_discrete_map={"Present": "#22C55E", "Absent": PRIMARY},
             template=PLOTLY_TEMPLATE, labels={"casualties": "Avg. Casualties", "traffic_signal_label": "Traffic Signal"})
fig.update_traces(textposition="outside")
fig.update_layout(height=CHART_H, showlegend=False, margin=dict(t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

st.write("")
render_insight_recommendation_panels(
    generate_casualty_insights(df), generate_casualty_recommendations(df),
    insight_caption="Where casualties concentrate by road type and signal presence.",
    rec_caption="Casualty-reduction focused actions.",
)