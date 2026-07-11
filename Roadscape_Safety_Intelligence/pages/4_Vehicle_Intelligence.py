"""Page 4 — Vehicle Intelligence

Note: the RoadScape dataset records vehicles_involved (a count per accident),
not individual vehicle records — so it has no vehicle type or vehicle age
fields. This page analyzes accident patterns through the vehicles_involved
lens instead, and is transparent about that scope.
"""

import plotly.express as px
import streamlit as st

from utils import (
    CHART_H, PLOTLY_TEMPLATE, PRIMARY, SEVERITY_COLORS,
    generate_vehicle_insights, generate_vehicle_recommendations, inject_global_css,
    load_raw_data, no_data_stop, page_header, render_filters, render_logo,
    render_insight_recommendation_panels, section_title,
)

st.set_page_config(page_title="RoadScape | Vehicle Intelligence", page_icon="🚘", layout="wide")
inject_global_css()

with st.sidebar:
    render_logo()

df_raw, load_error = load_raw_data()
if df_raw is None:
    st.error("Dataset not loaded. Go to the Executive Dashboard page and load the data first.")
    st.stop()

df = render_filters(df_raw)
page_header("🚘 Vehicle Intelligence", "How many vehicles are typically involved, and how does that relate to outcomes?")
if df.empty:
    no_data_stop()

st.markdown(
    '<div class="rs-note-box">ℹ️ This dataset logs <b>vehicles_involved</b> (a count per accident), '
    'not individual vehicle records — so it doesn\'t contain a vehicle type or vehicle age field. '
    'This page analyzes accident patterns through the vehicles-involved count instead of vehicle-type '
    'breakdowns.</div>',
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2, gap="large")
with c1:
    section_title("Vehicles Involved — Distribution")
    veh = df["vehicles_involved"].value_counts().sort_index().reset_index()
    veh.columns = ["vehicles_involved", "count"]
    fig = px.bar(veh, x="vehicles_involved", y="count", text="count",
                 color_discrete_sequence=[PRIMARY], template=PLOTLY_TEMPLATE,
                 labels={"vehicles_involved": "Vehicles Involved", "count": "Accidents"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    section_title("Vehicles Involved vs. Avg. Casualties")
    vc = df.groupby("vehicles_involved")["casualties"].mean().reset_index()
    fig = px.line(vc, x="vehicles_involved", y="casualties", markers=True,
                  color_discrete_sequence=["#3B9CFF"], template=PLOTLY_TEMPLATE,
                  labels={"casualties": "Avg. Casualties"})
    fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2, gap="large")
with c3:
    section_title("Vehicles Involved by Severity")
    fig = px.box(df, x="accident_severity", y="vehicles_involved", color="accident_severity",
                 color_discrete_map=SEVERITY_COLORS, template=PLOTLY_TEMPLATE,
                 category_orders={"accident_severity": ["minor", "major", "fatal"]})
    fig.update_layout(height=CHART_H, showlegend=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    section_title("Top States by Total Vehicles Involved")
    sv = df.groupby("state")["vehicles_involved"].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(sv, x="vehicles_involved", y="state", orientation="h", text="vehicles_involved",
                 color="vehicles_involved", color_continuous_scale="Reds", template=PLOTLY_TEMPLATE,
                 labels={"vehicles_involved": "Total Vehicles Involved"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

section_title("Vehicles Involved by Accident Cause")
vcause = df.groupby("cause")["vehicles_involved"].mean().sort_values(ascending=False).reset_index()
fig = px.bar(vcause, x="cause", y="vehicles_involved", text=vcause["vehicles_involved"].round(2),
             color="vehicles_involved", color_continuous_scale="Purples", template=PLOTLY_TEMPLATE,
             labels={"vehicles_involved": "Avg. Vehicles Involved"})
fig.update_traces(textposition="outside")
fig.update_layout(height=CHART_H, coloraxis_showscale=False, margin=dict(t=10, b=10),
                   paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

st.write("")
render_insight_recommendation_panels(
    generate_vehicle_insights(df), generate_vehicle_recommendations(df),
    insight_caption="How vehicle counts relate to severity and cause.",
    rec_caption="Multi-vehicle and cause-specific safety actions.",
)