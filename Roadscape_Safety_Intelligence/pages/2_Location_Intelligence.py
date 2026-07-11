"""Page 2 — Location Intelligence"""

import plotly.express as px
import streamlit as st

from utils import (
    CHART_H, PLOTLY_TEMPLATE, PRIMARY, SEVERITY_COLORS, inject_global_css,
    generate_location_insights, generate_location_recommendations, load_raw_data,
    no_data_stop, page_header, render_filters, render_logo,
    render_insight_recommendation_panels, section_title,
)

st.set_page_config(page_title="RoadScape | Location Intelligence", page_icon="📍", layout="wide")
inject_global_css()

with st.sidebar:
    render_logo()

df_raw, load_error = load_raw_data()
if df_raw is None:
    st.error("Dataset not loaded. Go to the Executive Dashboard page and load the data first.")
    st.stop()

df = render_filters(df_raw)
page_header("📍 Location Intelligence", "Where are accidents happening the most?")
if df.empty:
    no_data_stop()

# ----------------------------------------------------------------------------
section_title("Accident Hotspot Map", "Marker size = vehicles involved · color = severity")
map_sample = df.sample(min(len(df), 4000), random_state=42) if len(df) > 4000 else df
fig = px.scatter_mapbox(
    map_sample, lat="latitude", lon="longitude",
    color="accident_severity", size="vehicles_involved",
    color_discrete_map=SEVERITY_COLORS,
    hover_data={"city": True, "state": True, "cause": True, "casualties": True,
                "latitude": False, "longitude": False},
    zoom=3.6, height=520, mapbox_style="carto-darkmatter",
    center={"lat": 22.5, "lon": 79.5},
)
fig.update_layout(margin=dict(t=10, b=0, l=0, r=0), legend_title_text="Severity",
                   paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    section_title("Top Accident States")
    state_acc = df.groupby("state").size().sort_values(ascending=False).reset_index(name="Accidents")
    fig = px.bar(state_acc, x="Accidents", y="state", orientation="h", text="Accidents",
                 color="Accidents", color_continuous_scale="Reds", template=PLOTLY_TEMPLATE)
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    section_title("Urban vs Rural vs Highway", "Based on road_type — the closest available proxy for an urban/rural split")
    rt = df.groupby("road_type").size().sort_values(ascending=False).reset_index(name="Accidents")
    fig = px.pie(rt, names="road_type", values="Accidents", hole=0.5,
                 color_discrete_sequence=px.colors.sequential.Reds_r, template=PLOTLY_TEMPLATE)
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), showlegend=False,
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2, gap="large")
with c3:
    section_title("Top 10 Accident-Prone Cities", "This dataset records city-level, not district-level, geography")
    city_acc = df.groupby("city").size().sort_values(ascending=False).head(10).reset_index(name="Accidents")
    fig = px.bar(city_acc, x="Accidents", y="city", orientation="h", text="Accidents",
                 color="Accidents", color_continuous_scale="Blues", template=PLOTLY_TEMPLATE)
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    section_title("Average Casualties per Accident by State")
    state_cas = df.groupby("state")["casualties"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(state_cas, x="casualties", y="state", orientation="h",
                 text=state_cas["casualties"].round(2), color="casualties",
                 color_continuous_scale="Oranges", template=PLOTLY_TEMPLATE,
                 labels={"casualties": "Avg. Casualties"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False, margin=dict(t=10, b=10),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

section_title("City × Severity Breakdown (Top 10 Cities)")
top_cities = df.groupby("city").size().sort_values(ascending=False).head(10).index
cs = df[df["city"].isin(top_cities)].groupby(["city", "accident_severity"], observed=True).size().reset_index(name="Accidents")
fig = px.bar(cs, x="city", y="Accidents", color="accident_severity", barmode="stack",
             color_discrete_map=SEVERITY_COLORS, template=PLOTLY_TEMPLATE,
             category_orders={"city": list(top_cities)})
fig.update_layout(height=CHART_H, margin=dict(t=10, b=10), legend_title_text="Severity",
                   paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    '<div class="rs-note-box">ℹ️ The dataset records accidents at <b>city + state</b> level with '
    'latitude/longitude for hotspot mapping. It does not include a separate district field, so '
    '"district-wise analysis" above is shown at city granularity instead.</div>',
    unsafe_allow_html=True,
)

st.write("")
render_insight_recommendation_panels(
    generate_location_insights(df), generate_location_recommendations(df),
    insight_caption="Patterns across cities, road types, and states.",
    rec_caption="Location-specific safety actions.",
)