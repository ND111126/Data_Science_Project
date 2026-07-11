"""
utils.py — Shared utilities for the RoadScape Safety Intelligence Platform.
Theme constants, data loading, sidebar filters, and reusable UI components
used across every page of the multipage Streamlit app.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# =============================================================================
# THEME — dark, professional BI palette
# =============================================================================
BG = "#0B0E14"
BG_SIDEBAR = "#0A0C11"
CARD = "#141821"
CARD_BORDER = "#232838"
TEXT = "#E7EAF2"
MUTED = "#8B93A7"

PRIMARY = "#FF3B4E"     # signal red — danger / severity
ACCENT = "#F5A623"      # amber — caution
SUCCESS = "#22C55E"     # green — safe / low risk
INFO = "#3B9CFF"        # blue — informational
TEAL = "#2DD4BF"        # teal — secondary accent, variety
VIOLET = "#A78BFA"      # violet — secondary accent, variety
SKY = "#38BDF8"         # sky blue — secondary accent, variety
GOLD = "#FBBF24"        # gold — secondary accent, variety

# Rotating continuous color scales so different sections don't all look like
# the same red bar chart repeated
SCALE_A = "Tealgrn"
SCALE_B = "Sunsetdark"
SCALE_C = "Purp"
SCALE_D = "Agsunset"

SEVERITY_ORDER = ["minor", "major", "fatal"]
SEVERITY_COLORS = {"minor": SUCCESS, "major": ACCENT, "fatal": PRIMARY}

MONTH_ORDER = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
PERIOD_ORDER = ["Morning", "Afternoon", "Evening", "Night"]

PLOTLY_TEMPLATE = "plotly_dark"

# Standard chart height so every visualization across the app lines up neatly
CHART_H = 360

REQUIRED_COLS = [
    "city", "state", "latitude", "longitude", "date", "time", "day_of_week",
    "road_type", "traffic_signal", "weather", "visibility", "traffic_density",
    "cause", "accident_severity", "vehicles_involved", "casualties",
]

DATA_PATH_DEFAULT = Path(__file__).parent / "data" / "indian_roads_dataset21.xlsx"

# =============================================================================
# GLOBAL CSS
# =============================================================================
def inject_global_css():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {BG};
                color: {TEXT};
            }}
            #MainMenu, footer {{visibility: hidden;}}

            section[data-testid="stSidebar"] {{
                background-color: {BG_SIDEBAR};
                border-right: 1px solid {CARD_BORDER};
            }}
            section[data-testid="stSidebar"] * {{
                color: {TEXT} !important;
            }}
            section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
                background-color: {PRIMARY} !important;
            }}

            .rs-logo {{
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 6px 0 14px 0;
                border-bottom: 1px solid {CARD_BORDER};
                margin-bottom: 14px;
            }}
            .rs-logo-text h2 {{
                margin: 0;
                font-size: 1.25rem;
                font-weight: 800;
                letter-spacing: -0.4px;
                color: {TEXT};
            }}
            .rs-logo-text p {{
                margin: 0;
                font-size: 0.7rem;
                color: {MUTED};
                letter-spacing: 0.4px;
                text-transform: uppercase;
            }}

            .rs-sidebar-meta {{
                background: {CARD};
                border: 1px solid {CARD_BORDER};
                border-radius: 10px;
                padding: 10px 12px;
                margin-bottom: 16px;
                font-size: 0.76rem;
                color: {MUTED};
                line-height: 1.6;
            }}
            .rs-sidebar-meta b {{ color: {TEXT}; }}

            .rs-filter-group-label {{
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.6px;
                text-transform: uppercase;
                color: {MUTED};
                margin: 14px 0 2px 0;
            }}

            .rs-hero {{
                background: linear-gradient(120deg, #12141C 0%, #171A24 55%, #1D1420 140%);
                border: 1px solid {CARD_BORDER};
                padding: 26px 30px;
                border-radius: 14px;
                margin-bottom: 20px;
            }}
            .rs-hero h1 {{
                margin: 0;
                font-size: 1.9rem;
                font-weight: 800;
                letter-spacing: -0.5px;
                color: {TEXT};
            }}
            .rs-hero p {{
                margin: 6px 0 0 0;
                color: {MUTED};
                font-size: 0.95rem;
                max-width: 780px;
            }}
            .rs-hero .rs-hero-tagline {{
                color: {ACCENT};
                font-weight: 600;
                font-size: 0.88rem;
                margin-top: 10px;
                font-style: italic;
            }}
            .rs-badge {{
                display: inline-block;
                background: {CARD};
                border: 1px solid {CARD_BORDER};
                color: {MUTED};
                padding: 3px 12px;
                border-radius: 20px;
                font-size: 0.74rem;
                margin-top: 12px;
                margin-right: 6px;
            }}

            div[data-testid="stMetric"] {{
                background: {CARD};
                border: 1px solid {CARD_BORDER};
                border-top: 3px solid {PRIMARY};
                border-radius: 12px;
                padding: 14px 16px 10px 16px;
            }}
            div[data-testid="stMetricLabel"] {{
                font-weight: 600;
                color: {MUTED};
            }}
            div[data-testid="stMetricValue"] {{
                color: {TEXT};
            }}
            div[data-testid="column"]:nth-of-type(6n+2) div[data-testid="stMetric"] {{ border-top-color: {ACCENT}; }}
            div[data-testid="column"]:nth-of-type(6n+3) div[data-testid="stMetric"] {{ border-top-color: {VIOLET}; }}
            div[data-testid="column"]:nth-of-type(6n+4) div[data-testid="stMetric"] {{ border-top-color: {PRIMARY}; }}
            div[data-testid="column"]:nth-of-type(6n+5) div[data-testid="stMetric"] {{ border-top-color: {SKY}; }}
            div[data-testid="column"]:nth-of-type(6n+6) div[data-testid="stMetric"] {{ border-top-color: {TEAL}; }}

            /* Breathing room between charts and section blocks so nothing feels congested */
            div[data-testid="stPlotlyChart"] {{
                margin-bottom: 6px;
                padding: 6px;
            }}
            div[data-testid="stHorizontalBlock"] {{
                gap: 1.75rem;
                margin-bottom: 8px;
            }}
            div[data-testid="stVerticalBlockBorderWrapper"] {{
                margin-bottom: 10px;
            }}

            .rs-section-block {{
                margin-top: 38px;
                margin-bottom: 6px;
            }}
            .rs-section-title {{
                font-size: 1.08rem;
                font-weight: 700;
                color: {TEXT};
                margin-top: 4px;
                margin-bottom: 2px;
                border-left: 4px solid {PRIMARY};
                padding-left: 10px;
            }}
            .rs-section-eyebrow {{
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 1.2px;
                text-transform: uppercase;
                color: {PRIMARY};
                padding-left: 10px;
                margin-bottom: 2px;
            }}
            .rs-caption {{
                color: {MUTED};
                font-size: 0.84rem;
                padding-left: 14px;
                margin-bottom: 10px;
            }}
            .rs-page-title {{
                font-size: 1.6rem;
                font-weight: 800;
                color: {TEXT};
                margin-bottom: 0px;
            }}
            .rs-page-sub {{
                color: {MUTED};
                margin-bottom: 18px;
                font-size: 0.95rem;
            }}

            .rs-divider {{
                border: none;
                border-top: 1px solid {CARD_BORDER};
                margin: 30px 0 18px 0;
            }}

            .rs-insight-box {{
                background: #1B1712;
                border-left: 4px solid {ACCENT};
                padding: 12px 16px;
                border-radius: 8px;
                font-size: 0.92rem;
                color: #F0DDB4;
                margin: 8px 0 14px 0;
            }}
            .rs-recommend-box {{
                background: #10201A;
                border-left: 4px solid {SUCCESS};
                padding: 12px 16px;
                border-radius: 8px;
                font-size: 0.92rem;
                color: #C7EFDA;
                margin: 8px 0 14px 0;
            }}
            .rs-note-box {{
                background: #10161F;
                border-left: 4px solid {INFO};
                padding: 12px 16px;
                border-radius: 8px;
                font-size: 0.86rem;
                color: {MUTED};
                margin: 8px 0 14px 0;
            }}
            .rs-summary-box {{
                background: {CARD};
                border: 1px solid {CARD_BORDER};
                border-top: 3px solid {ACCENT};
                padding: 18px 22px;
                border-radius: 12px;
                font-size: 0.95rem;
                color: {TEXT};
                line-height: 1.65;
                margin: 10px 0 18px 0;
            }}

            .stTabs [data-baseweb="tab"] {{
                background-color: {CARD};
                border-radius: 8px 8px 0 0;
                padding: 8px 16px;
                font-weight: 600;
                color: {MUTED};
            }}
            .stTabs [aria-selected="true"] {{
                background-color: {PRIMARY} !important;
                color: white !important;
            }}

            [data-testid="stDataFrame"] {{
                border: 1px solid {CARD_BORDER};
                border-radius: 8px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_logo():
    st.markdown(
        """
        <div class="rs-logo">
            <div style="font-size:1.8rem;">🚦</div>
            <div class="rs-logo-text">
                <h2>RoadScape</h2>
                <p>Safety Intelligence Platform</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = ""):
    st.markdown(f'<div class="rs-page-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="rs-page-sub">{subtitle}</div>', unsafe_allow_html=True)


def section_title(text: str, caption: str = "", eyebrow: str = ""):
    st.markdown('<div class="rs-section-block"></div>', unsafe_allow_html=True)
    if eyebrow:
        st.markdown(f'<p class="rs-section-eyebrow">{eyebrow}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="rs-section-title">{text}</p>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<p class="rs-caption">{caption}</p>', unsafe_allow_html=True)


# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data(show_spinner=True)
def _read_excel(file) -> pd.DataFrame:
    return pd.read_excel(file)


@st.cache_data(show_spinner=True)
def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing expected columns: {missing}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["time_str"] = df["time"].astype(str)
    df["hour"] = pd.to_datetime(df["time_str"], format="%H:%M:%S", errors="coerce").dt.hour
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month

    def time_period(h):
        if pd.isna(h):
            return "Unknown"
        if 5 <= h < 12:
            return "Morning"
        elif 12 <= h < 17:
            return "Afternoon"
        elif 17 <= h < 21:
            return "Evening"
        return "Night"

    df["time_period"] = df["hour"].apply(time_period)
    df["accident_severity"] = pd.Categorical(
        df["accident_severity"], categories=SEVERITY_ORDER, ordered=True
    )
    df["traffic_signal_label"] = df["traffic_signal"].map({1: "Present", 0: "Absent"})
    df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])
    df["day_type"] = df["is_weekend"].map({True: "Weekend", False: "Weekday"})
    return df


def load_raw_data():
    """Loads from sidebar upload (session-cached) or the bundled data/ file."""
    if "uploaded_bytes" not in st.session_state:
        st.session_state["uploaded_bytes"] = None

    with st.sidebar:
        uploaded = st.file_uploader(
            "Load dataset (.xlsx)", type=["xlsx"], key="global_uploader",
            help="Optional — the app already ships with the RoadScape dataset. "
                 "Upload a file only if you want to analyze a different one.",
        )
        if uploaded is not None:
            st.session_state["uploaded_bytes"] = uploaded.getvalue()
            st.session_state["uploaded_name"] = uploaded.name

    try:
        if st.session_state["uploaded_bytes"] is not None:
            import io
            raw = _read_excel(io.BytesIO(st.session_state["uploaded_bytes"]))
        else:
            raw = _read_excel(DATA_PATH_DEFAULT)
        return prepare_data(raw), None
    except FileNotFoundError:
        return None, "not_found"
    except Exception as e:
        return None, str(e)


# =============================================================================
# SIDEBAR FILTERS (state persists across pages via st.session_state keys)
# =============================================================================
FILTER_KEYS = [
    "f_year", "f_state", "f_city", "f_weather", "f_severity", "f_road",
    "f_period", "f_traffic", "f_visibility", "f_daytype",
]


def render_filters(df_raw: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.markdown(
            f"""
            <div class="rs-sidebar-meta">
            📦 <b>{len(df_raw):,}</b> total records<br>
            🗺️ <b>{df_raw['state'].nunique()}</b> states · 🏙️ <b>{df_raw['city'].nunique()}</b> cities<br>
            📅 <b>{df_raw['date'].min().strftime('%b %Y')}</b> – <b>{df_raw['date'].max().strftime('%b %Y')}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 🔎 Filters")

        years = sorted(df_raw["year"].unique())
        states = sorted(df_raw["state"].unique())
        cities = sorted(df_raw["city"].unique())
        weathers = sorted(df_raw["weather"].unique())
        roads = sorted(df_raw["road_type"].unique())
        traffic_levels = sorted(df_raw["traffic_density"].unique())
        visibilities = sorted(df_raw["visibility"].unique())
        day_types = sorted(df_raw["day_type"].unique())

        st.markdown('<p class="rs-filter-group-label">🕐 Time</p>', unsafe_allow_html=True)
        st.multiselect("📅 Year", years, default=years, key="f_year")
        st.multiselect("⏱️ Time Period", PERIOD_ORDER, default=PERIOD_ORDER, key="f_period")
        st.multiselect("📆 Day Type", day_types, default=day_types, key="f_daytype")

        st.markdown('<p class="rs-filter-group-label">📍 Location</p>', unsafe_allow_html=True)
        st.multiselect("🗺️ State", states, default=states, key="f_state")
        st.multiselect("🏙️ City", cities, default=cities, key="f_city")
        st.multiselect("🛣️ Road Type", roads, default=roads, key="f_road")

        st.markdown('<p class="rs-filter-group-label">🌦️ Conditions</p>', unsafe_allow_html=True)
        st.multiselect("🌧️ Weather", weathers, default=weathers, key="f_weather")
        st.multiselect("👁️ Visibility", visibilities, default=visibilities, key="f_visibility")
        st.multiselect("🚦 Traffic Density", traffic_levels, default=traffic_levels, key="f_traffic")

        st.markdown('<p class="rs-filter-group-label">🚑 Outcome</p>', unsafe_allow_html=True)
        st.multiselect("⚠️ Severity", SEVERITY_ORDER, default=SEVERITY_ORDER, key="f_severity")

        st.write("")
        if st.button("↺ Reset filters", use_container_width=True):
            for k in FILTER_KEYS:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

        st.divider()
        st.caption("Python · Pandas · Plotly · Streamlit")
        st.caption("O7 Services — Data Analytics Internship")

    f_year = st.session_state.get("f_year", years)
    f_state = st.session_state.get("f_state", states)
    f_city = st.session_state.get("f_city", cities)
    f_weather = st.session_state.get("f_weather", weathers)
    f_severity = st.session_state.get("f_severity", SEVERITY_ORDER)
    f_road = st.session_state.get("f_road", roads)
    f_period = st.session_state.get("f_period", PERIOD_ORDER)
    f_traffic = st.session_state.get("f_traffic", traffic_levels)
    f_visibility = st.session_state.get("f_visibility", visibilities)
    f_daytype = st.session_state.get("f_daytype", day_types)

    mask = (
        df_raw["year"].isin(f_year)
        & df_raw["state"].isin(f_state)
        & df_raw["city"].isin(f_city)
        & df_raw["weather"].isin(f_weather)
        & df_raw["accident_severity"].isin(f_severity)
        & df_raw["road_type"].isin(f_road)
        & df_raw["time_period"].isin(f_period)
        & df_raw["traffic_density"].isin(f_traffic)
        & df_raw["visibility"].isin(f_visibility)
        & df_raw["day_type"].isin(f_daytype)
    )
    return df_raw[mask].copy()


def kpi_row(df: pd.DataFrame):
    total_accidents = len(df)
    total_casualties = int(df["casualties"].sum())
    serious_casualties = int(df.loc[df["accident_severity"].isin(["major", "fatal"]), "casualties"].sum())
    fatal_casualties = int(df.loc[df["accident_severity"] == "fatal", "casualties"].sum())
    total_vehicles = int(df["vehicles_involved"].sum())
    avg_casualties = (total_casualties / total_accidents) if total_accidents else 0.0

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("🚗 Total Accidents", f"{total_accidents:,}")
    c2.metric("💀 Total Casualties", f"{total_casualties:,}")
    c3.metric("🚑 Serious Casualties", f"{serious_casualties:,}")
    c4.metric("☠️ Fatal Casualties", f"{fatal_casualties:,}")
    c5.metric("🚙 Total Vehicles Involved", f"{total_vehicles:,}")
    c6.metric("📊 Avg Casualties / Accident", f"{avg_casualties:.2f}")


def no_data_stop():
    st.warning("No records match the current filter selection. Adjust the filters in the sidebar.")
    st.stop()


# =============================================================================
# AUTOMATED INSIGHTS & RECOMMENDATIONS
# (reusable across every page — pass in the filtered df, get back plain-language
#  observations. Keeps the "smart" logic in one place instead of copy-pasted.)
# =============================================================================
def generate_overview_insights(df: pd.DataFrame) -> list[str]:
    """Big-picture stats for the Overview Dashboard only."""
    if df.empty:
        return ["No records match the current filters — try widening your selection."]
    total = len(df)
    top_state = df["state"].value_counts()
    fatal_share = (df["accident_severity"] == "fatal").mean() * 100
    top_cause = df["cause"].value_counts().idxmax()
    return [
        f"**{top_state.index[0]}** leads with **{top_state.iloc[0]:,}** accidents "
        f"({top_state.iloc[0] / total * 100:.1f}% of the current selection).",
        f"**{fatal_share:.1f}%** of accidents recorded here are fatal.",
        f"**{top_cause.title()}** is the single largest recorded cause across all accidents.",
    ]


def generate_location_insights(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return ["No records match the current filters."]
    city_counts = df["city"].value_counts()
    road_counts = df["road_type"].value_counts()
    top_city_share = city_counts.iloc[0] / len(df) * 100
    state_cas = df.groupby("state")["casualties"].mean().sort_values(ascending=False)
    return [
        f"**{city_counts.index[0]}** is the single busiest city, accounting for "
        f"**{top_city_share:.1f}%** of all accidents in this selection.",
        f"**{road_counts.index[0].title()}** roads carry the largest share of recorded accidents "
        f"({road_counts.iloc[0]:,} of {len(df):,}).",
        f"**{state_cas.index[0]}** has the highest average casualties per accident "
        f"({state_cas.iloc[0]:.2f}) among all states, even if it isn't the highest-volume state.",
    ]


def generate_location_recommendations(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return []
    city_counts = df["city"].value_counts()
    road_counts = df["road_type"].value_counts()
    return [
        f"Deploy speed cameras and traffic police at hotspot junctions in "
        f"**{city_counts.index[0]}**, the highest-frequency city.",
        f"Review lane markings and speed limits on **{road_counts.index[0].title()}** stretches, "
        f"which see the most accidents by road type.",
        "Add reflective hotspot signage at the top clusters shown on the map above.",
    ]


def generate_weather_insights(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return ["No records match the current filters."]
    bad_weather = df[df["weather"].isin(["rain", "fog"])]
    bad_weather_fatal = (bad_weather["accident_severity"] == "fatal").mean() * 100 if not bad_weather.empty else 0
    clear_fatal = (df[~df["weather"].isin(["rain", "fog"])]["accident_severity"] == "fatal").mean() * 100
    low_vis_share = (df["visibility"] == "low").mean() * 100
    signal_absent_share = (df["traffic_signal_label"] == "Absent").mean() * 100
    return [
        f"Accidents in rain/fog turn fatal **{bad_weather_fatal:.1f}%** of the time, versus "
        f"**{clear_fatal:.1f}%** in clearer conditions.",
        f"**{low_vis_share:.1f}%** of all accidents in this selection occur under low visibility.",
        f"**{signal_absent_share:.1f}%** of accidents happen where no traffic signal is present.",
    ]


def generate_weather_recommendations(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return []
    return [
        "Improve road drainage and add anti-skid surfacing on stretches prone to rain-related accidents.",
        "Install reflective lane markers and street lighting where low-visibility accidents cluster.",
        "Push visibility-based dynamic speed advisories during fog and heavy rain.",
    ]


def generate_vehicle_insights(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return ["No records match the current filters."]
    vs = df.groupby("accident_severity", observed=True)["vehicles_involved"].mean()
    multi_vehicle_share = (df["vehicles_involved"] >= 3).mean() * 100
    top_cause_vehicles = df.groupby("cause")["vehicles_involved"].mean().sort_values(ascending=False)
    return [
        f"Average vehicles involved rises with severity: "
        + " → ".join(f"{s} {vs.get(s, 0):.2f}" for s in ["minor", "major", "fatal"]) + ".",
        f"**{multi_vehicle_share:.1f}%** of accidents in this selection involve 3 or more vehicles.",
        f"**{top_cause_vehicles.index[0].title()}** accidents involve the most vehicles on average "
        f"({top_cause_vehicles.iloc[0]:.2f}).",
    ]


def generate_vehicle_recommendations(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return []
    return [
        "Target multi-vehicle pile-up corridors with mandatory speed governors on commercial vehicles.",
        "Run cause-specific driver awareness campaigns where average vehicles-involved is highest.",
        "Encourage safe following-distance messaging on high-density routes.",
    ]


def generate_casualty_insights(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return ["No records match the current filters."]
    rc = df.groupby("road_type")["casualties"].mean().sort_values(ascending=False)
    tsc = df.groupby("traffic_signal_label")["casualties"].mean()
    cc = df.groupby("cause")["casualties"].sum().sort_values(ascending=False)
    return [
        f"**{rc.index[0].title()}** roads have the highest average casualties per accident "
        f"({rc.iloc[0]:.2f}).",
        f"Accidents with **no traffic signal present** average "
        f"{tsc.get('Absent', 0):.2f} casualties vs {tsc.get('Present', 0):.2f} where one is present.",
        f"**{cc.index[0].title()}** contributes the most total casualties of any recorded cause "
        f"({int(cc.iloc[0]):,}).",
    ]


def generate_casualty_recommendations(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return []
    return [
        "Prioritize faster ambulance dispatch and trauma-care readiness on the highest-casualty road types.",
        "Fast-track signal installation at high-casualty, signal-absent locations.",
        "Pair cause-specific enforcement with post-accident emergency-response drills.",
    ]


def generate_time_insights(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return ["No records match the current filters."]
    hourly = df.dropna(subset=["hour"]).groupby("hour").size()
    peak_hour = int(hourly.idxmax()) if not hourly.empty else None
    weekend_share = (df["day_type"] == "Weekend").mean() * 100
    top_day = df["day_of_week"].value_counts().reindex(DAY_ORDER).idxmax()
    peak_txt = f"**{peak_hour}:00–{peak_hour + 1}:00**" if peak_hour is not None else "an undetermined hour"
    return [
        f"The single busiest hour is {peak_txt}.",
        f"**{top_day}** records the highest accident frequency among all days of the week.",
        f"Weekends make up **{weekend_share:.1f}%** of accidents despite being only 2 of 7 days.",
    ]


def generate_time_recommendations(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return []
    return [
        "Shift patrol rosters to cover the identified peak hour with extra staffing.",
        "Plan targeted weekend enforcement if weekend share is disproportionately high.",
        "Align emergency-response shift changes away from the peak accident window.",
    ]


def render_insight_recommendation_panels(insights: list[str], recommendations: list[str],
                                          insight_caption: str = "What the data shows",
                                          rec_caption: str = "Suggested next steps"):
    """Renders two side-by-side panels from pre-computed, page-specific
    insight and recommendation lists (pass in the output of one of the
    generate_*_insights / generate_*_recommendations functions above so each
    page shows genuinely different content instead of repeating the same
    generic observations)."""
    col1, col2 = st.columns(2, gap="large")
    with col1:
        section_title("🔎 Key Insights", insight_caption)
        for point in insights:
            st.markdown(f'<div class="rs-insight-box">💡 {point}</div>', unsafe_allow_html=True)
    with col2:
        section_title("✅ Recommendations", rec_caption)
        for point in recommendations:
            st.markdown(f'<div class="rs-recommend-box">➤ {point}</div>', unsafe_allow_html=True)


def generate_executive_summary(df: pd.DataFrame) -> str:
    """Returns a short auto-generated paragraph summarizing the most important
    findings from the currently filtered dataset — used for the Executive
    Summary block at the bottom of the Overview Dashboard."""
    if df.empty:
        return "No records match the current filter selection."

    total = len(df)
    total_casualties = int(df["casualties"].sum())
    fatal_share = (df["accident_severity"] == "fatal").mean() * 100
    top_state = df["state"].value_counts().idxmax()
    top_state_n = df["state"].value_counts().max()
    top_cause = df["cause"].value_counts().idxmax()
    top_weather = df["weather"].value_counts().idxmax()
    hourly = df.dropna(subset=["hour"]).groupby("hour").size()
    peak_hour = int(hourly.idxmax()) if not hourly.empty else None
    top_period = df["time_period"].value_counts().idxmax()

    peak_hour_txt = f"around **{peak_hour}:00**" if peak_hour is not None else "at an undetermined hour"

    return (
        f"Across the current selection of **{total:,} accidents**, resulting in "
        f"**{total_casualties:,} total casualties**, **{top_state}** records the highest number of "
        f"incidents (**{top_state_n:,}**). **{fatal_share:.1f}%** of accidents are fatal. "
        f"**{top_cause.title()}** is the leading recorded cause, and accidents concentrate in the "
        f"**{top_period.lower()}** window, peaking {peak_hour_txt}. **{top_weather.title()}** weather is "
        f"the most frequently recorded condition among accidents in this view. Together, these patterns "
        f"point to targeted enforcement, awareness campaigns, and infrastructure investment as the "
        f"highest-leverage next steps."
    )


def download_csv_button(df: pd.DataFrame, filename="roadscape_filtered_data.csv"):
    st.download_button(
        "⬇️ Download filtered data as CSV",
        df.drop(columns=["time_str"], errors="ignore").to_csv(index=False).encode("utf-8"),
        file_name=filename, mime="text/csv", use_container_width=False,
    )


def render_data_table(df: pd.DataFrame, height: int = 360):
    """Improved, readable data table: relevant columns only, most recent
    records first, with a download button placed right beside it."""
    display_cols = [
        "date", "time", "city", "state", "road_type", "weather", "visibility",
        "traffic_density", "cause", "accident_severity", "vehicles_involved", "casualties",
    ]
    display_cols = [c for c in display_cols if c in df.columns]
    table_df = df[display_cols].sort_values("date", ascending=False).reset_index(drop=True)

    hcol, dcol = st.columns([4, 1])
    with hcol:
        st.caption(f"Showing {len(table_df):,} filtered records, most recent first.")
    with dcol:
        download_csv_button(df)

    st.dataframe(table_df, use_container_width=True, height=height)


def compute_risk_table(df: pd.DataFrame) -> pd.DataFrame:
    """Composite RoadScape Risk Score (30/25/20/10/10/5% weighting),
    with quantile-based Low/Medium/High tiering."""
    risk_df = (
        df.groupby("state")
        .agg(
            Total_Accidents=("state", "count"),
            Avg_Casualties=("casualties", "mean"),
            Severe_Accidents=("accident_severity", lambda x: (x == "fatal").sum()),
            High_Traffic=("traffic_density", lambda x: (x == "high").sum()),
            Bad_Weather=("weather", lambda x: x.isin(["rain", "fog"]).sum()),
            Poor_visibility=("visibility", lambda x: (x == "low").sum()),
        )
        .reset_index()
    )
    if risk_df.empty:
        return risk_df

    cols = ["Total_Accidents", "Avg_Casualties", "Severe_Accidents",
            "High_Traffic", "Bad_Weather", "Poor_visibility"]
    for col in cols:
        max_val = risk_df[col].max()
        risk_df[col + "_Score"] = (risk_df[col] / max_val * 100) if max_val else 0

    risk_df["Composite_Risk_Score"] = (
        0.30 * risk_df["Total_Accidents_Score"]
        + 0.25 * risk_df["Avg_Casualties_Score"]
        + 0.20 * risk_df["Severe_Accidents_Score"]
        + 0.10 * risk_df["High_Traffic_Score"]
        + 0.10 * risk_df["Poor_visibility_Score"]
        + 0.05 * risk_df["Bad_Weather_Score"]
    ).round(2)

    risk_df = risk_df.sort_values("Composite_Risk_Score", ascending=False).reset_index(drop=True)
    risk_df["Rank"] = range(1, len(risk_df) + 1)
    try:
        risk_df["Risk_Level"] = pd.qcut(
            risk_df["Composite_Risk_Score"], q=3, labels=["Low", "Medium", "High"]
        )
    except ValueError:
        risk_df["Risk_Level"] = pd.cut(
            risk_df["Composite_Risk_Score"], bins=3, labels=["Low", "Medium", "High"]
        )

    def recommendation(level):
        if level == "High":
            return "Increase traffic surveillance, improve road infrastructure, and strengthen emergency response."
        elif level == "Medium":
            return "Improve traffic monitoring, road maintenance, and conduct public awareness campaigns."
        return "Maintain current safety measures and continue regular monitoring."

    risk_df["Recommendation"] = risk_df["Risk_Level"].apply(recommendation)
    return risk_df