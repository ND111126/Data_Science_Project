"""
app.py — RoadScape Safety Intelligence Platform
Page 1: Overview Dashboard
"""
import plotly.express as px
import streamlit as st

from utils import (
    ACCENT, CHART_H, GOLD, PERIOD_ORDER, PLOTLY_TEMPLATE, PRIMARY, SCALE_A,
    SCALE_B, SEVERITY_COLORS, SEVERITY_ORDER, SKY, TEAL, VIOLET,
    generate_executive_summary, generate_overview_insights, inject_global_css,
    kpi_row, load_raw_data, no_data_stop, page_header, render_data_table,
    render_filters, render_logo, section_title,
)

st.set_page_config(page_title="RoadScape | Overview Dashboard", page_icon="🚦", layout="wide")
inject_global_css()

with st.sidebar:
    render_logo()

df_raw, load_error = load_raw_data()

if df_raw is None:
    page_header("🚦 RoadScape", "Road Safety Intelligence Platform")
    if load_error == "not_found":
        st.warning("Couldn't find the bundled dataset at `data/indian_roads_dataset21.xlsx`.")
    else:
        st.error(f"Couldn't load the dataset: {load_error}")
    st.info("Upload `indian_roads_dataset21.xlsx` using the sidebar to launch the dashboard.")
    st.stop()

df = render_filters(df_raw)
if df.empty:
    page_header("🚦 RoadScape", "Road Safety Intelligence Platform")
    no_data_stop()

# =============================================================================
# HERO BANNER
# =============================================================================
st.markdown(
    f"""
    <div class="rs-hero">
    <h1>🚦 RoadScape — Road Safety Intelligence Platform</h1>
    <p>
    A multi-page analytics dashboard turning Indian road accident records into clear,
    actionable safety intelligence — covering where accidents happen, why, and when.
    </p>
    <div class="rs-hero-tagline">📌From Data to Decisions, From Insights to Safety. </div>
    <span class="rs-badge">📊 Dataset: <b>{len(df_raw):,}</b> Records</span>
    <span class="rs-badge">🗺️ {df_raw['state'].nunique()} States</span>
    <span class="rs-badge">🏙️ {df_raw['city'].nunique()} Cities</span>
    <span class="rs-badge">📅 {df_raw['date'].min().strftime('%Y')} – {df_raw['date'].max().strftime('%Y')}</span>
    <span class="rs-badge">🔎 {len(df):,} Records Selected</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# KPI CARDS
# =============================================================================
kpi_row(df)

# =============================================================================
# ACCIDENT OVERVIEW
# =============================================================================
section_title("Accident Overview", "Year-over-year volume and severity split", eyebrow="TRENDS")

c1, c2 = st.columns(2, gap="large")
with c1:
    yearly = df.groupby("year").size().reset_index(name="Accidents")
    fig = px.bar(yearly, x="year", y="Accidents", text="Accidents",
                 color_discrete_sequence=[TEAL], template=PLOTLY_TEMPLATE,
                 title="Accidents by Year")
    fig.update_traces(textposition="outside", hovertemplate="Year %{x}<br>%{y:,} accidents<extra></extra>")
    fig.update_xaxes(dtick=1)
    fig.update_layout(height=CHART_H, margin=dict(t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    sev = df["accident_severity"].value_counts().reindex(SEVERITY_ORDER).reset_index()
    sev.columns = ["accident_severity", "count"]
    fig = px.pie(sev, names="accident_severity", values="count", hole=0.55,
                 color="accident_severity", color_discrete_map=SEVERITY_COLORS,
                 template=PLOTLY_TEMPLATE, title="Severity Distribution")
    fig.update_traces(textinfo="percent+label", hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>")
    fig.update_layout(height=CHART_H, margin=dict(t=40, b=20), legend_title_text="Severity",
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

ov_insights = generate_overview_insights(df)
st.markdown(f'<div class="rs-insight-box">📌 {ov_insights[0]}</div>', unsafe_allow_html=True)

# =============================================================================
# GEOGRAPHIC ANALYSIS
# =============================================================================
section_title("Geographic Analysis", "Highest-volume states and cities", eyebrow="GEOGRAPHY")

c3, c4 = st.columns(2, gap="large")
with c3:
    state_acc = df.groupby("state").size().sort_values(ascending=False).head(10).reset_index(name="Accidents")
    fig = px.bar(state_acc, x="Accidents", y="state", orientation="h", text="Accidents",
                 color="Accidents", color_continuous_scale=SCALE_A, template=PLOTLY_TEMPLATE,
                 title="Top 10 States by Accident Count")
    fig.update_traces(textposition="outside", hovertemplate="%{y}<br>%{x:,} accidents<extra></extra>")
    fig.update_layout(height=CHART_H, yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False, margin=dict(t=40, b=20),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    city_acc = df.groupby("city").size().sort_values(ascending=False).head(10).reset_index(name="Accidents")
    fig = px.bar(city_acc, x="Accidents", y="city", orientation="h", text="Accidents",
                 color="Accidents", color_continuous_scale=SCALE_B, template=PLOTLY_TEMPLATE,
                 title="Top 10 Cities by Accident Count")
    fig.update_traces(textposition="outside", hovertemplate="%{y}<br>%{x:,} accidents<extra></extra>")
    fig.update_layout(height=CHART_H, yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False, margin=dict(t=40, b=20),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

top_state = df["state"].value_counts().idxmax()
top_city = df["city"].value_counts().idxmax()
st.markdown(
    f'<div class="rs-recommend-box">✅ Prioritize enforcement and infrastructure spend in '
    f'<b>{top_state}</b> and <b>{top_city}</b> — the highest-volume state and city in this selection. '
    f'Full hotspot map is further down this page.</div>',
    unsafe_allow_html=True,
)

# =============================================================================
# CONDITIONS ANALYSIS (traffic + weather combined, keeps the page shorter)
# =============================================================================
section_title("Conditions Analysis", "Traffic density and weather patterns behind accidents",
              eyebrow="CONDITIONS")

c5, c6 = st.columns(2, gap="large")
with c5:
    td = df.groupby("traffic_density")["casualties"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(td, x="traffic_density", y="casualties", text=td["casualties"].round(2),
                 color_discrete_sequence=[VIOLET], template=PLOTLY_TEMPLATE,
                 title="Avg. Casualties by Traffic Density", labels={"casualties": "Avg. Casualties"})
    fig.update_traces(textposition="outside", hovertemplate="%{x}<br>%{y:.2f} avg casualties<extra></extra>")
    fig.update_layout(height=CHART_H, margin=dict(t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c6:
    w = df.groupby("weather").size().sort_values(ascending=False).reset_index(name="Accidents")
    fig = px.pie(w, names="weather", values="Accidents", hole=0.55,
                 color_discrete_sequence=[SKY, GOLD, TEAL, VIOLET, PRIMARY, ACCENT],
                 template=PLOTLY_TEMPLATE, title="Weather — Accident Share")
    fig.update_traces(textinfo="percent+label", hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>")
    fig.update_layout(height=CHART_H, margin=dict(t=40, b=20), showlegend=False,
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

top_weather = df["weather"].value_counts().idxmax()
signal_absent_share = (df["traffic_signal_label"] == "Absent").mean() * 100
st.markdown(
    f'<div class="rs-insight-box">📌 <b>{top_weather.title()}</b> is the most frequently recorded '
    f'weather condition, and <b>{signal_absent_share:.1f}%</b> of accidents occur where no traffic '
    f'signal is present. See the Weather &amp; Road Conditions page for the full breakdown.</div>',
    unsafe_allow_html=True,
)

# =============================================================================
# TIME ANALYSIS
# =============================================================================
section_title("Time Analysis", "When accidents happen across the day", eyebrow="TIMING")

c7, c8 = st.columns(2, gap="large")
with c7:
    hourly = df.dropna(subset=["hour"]).groupby("hour").size().reset_index(name="Accidents")
    peak_hour = int(hourly.loc[hourly["Accidents"].idxmax(), "hour"]) if not hourly.empty else None
    fig = px.line(hourly, x="hour", y="Accidents", markers=True,
                  color_discrete_sequence=[SKY], template=PLOTLY_TEMPLATE,
                  title="Hourly Accident Pattern (0–23h)")
    if peak_hour is not None:
        fig.add_vline(x=peak_hour, line_dash="dash", line_color=GOLD,
                       annotation_text=f"Peak: {peak_hour}:00", annotation_position="top")
    fig.update_xaxes(dtick=1)
    fig.update_layout(height=CHART_H, margin=dict(t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c8:
    period = df.groupby("time_period").size().reindex(PERIOD_ORDER).reset_index(name="Accidents")
    fig = px.bar(period, x="time_period", y="Accidents", text="Accidents",
                 color="time_period", template=PLOTLY_TEMPLATE, title="Accidents by Time Period",
                 color_discrete_map={"Morning": GOLD, "Afternoon": ACCENT,
                                     "Evening": VIOLET, "Night": "#1B2A4A"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=CHART_H, showlegend=False, margin=dict(t=40, b=20),
                       paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

top_period = df.groupby("time_period").size().reindex(PERIOD_ORDER).idxmax()
peak_hour_txt = f"{peak_hour}:00–{peak_hour + 1}:00" if peak_hour is not None else "an undetermined hour"
st.markdown(
    f'<div class="rs-recommend-box">✅ Focus patrols on the <b>{top_period.lower()}</b> window, '
    f'especially <b>{peak_hour_txt}</b>, the single busiest hour in this selection.</div>',
    unsafe_allow_html=True,
)

# =============================================================================
# INTERACTIVE ACCIDENT MAP
# =============================================================================
section_title("Interactive Accident Map", "Marker size = vehicles involved · color = severity",
              eyebrow="HOTSPOTS")

map_sample = df.sample(min(len(df), 4000), random_state=42) if len(df) > 4000 else df
fig = px.scatter_mapbox(
    map_sample, lat="latitude", lon="longitude",
    color="accident_severity", size="vehicles_involved",
    color_discrete_map=SEVERITY_COLORS,
    hover_data={"city": True, "state": True, "cause": True, "casualties": True,
                "weather": True, "latitude": False, "longitude": False},
    zoom=3.6, height=500, mapbox_style="carto-darkmatter",
    center={"lat": 22.5, "lon": 79.5},
)
fig.update_layout(margin=dict(t=10, b=0, l=0, r=0), legend_title_text="Severity",
                   paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# EXECUTIVE SUMMARY (one compact block instead of three separate ones)
# =============================================================================
section_title("Executive Summary", "The current selection, in one paragraph", eyebrow="SUMMARY")
st.markdown(f'<div class="rs-summary-box">{generate_executive_summary(df)}</div>', unsafe_allow_html=True)

# =============================================================================
# FILTERED DATA + DOWNLOAD
# =============================================================================
with st.expander("🔍 View filtered records"):
    render_data_table(df, height=320)

st.markdown('<hr class="rs-divider">', unsafe_allow_html=True)
