# 🚦 RoadScape — Safety Intelligence Platform

A resume-worthy, multi-page Streamlit BI dashboard analyzing 20,000+ Indian road accident records across 8 cities and 7 states.

🔗 **Live demo:** *https://datascienceproject-xjitenhpdcvo9n32r6susf.streamlit.app/*

---

## Project Structure

```
roadscape_dashboard/
├── Home.py                                 # Page 1 — Executive Dashboard (entry point)
├── utils.py                                # Shared theme, data loading, filters, KPI cards
├── requirements.txt
├── data/
│   └── indian_roads_dataset.xlsx         # Bundled dataset
├── assets/
│   └── logo.svg
└── pages/
    ├── 2_📍_Location_Intelligence.py
    ├── 3_⏰_Time_Intelligence.py
    ├── 4_🌦️_Weather_Road_Conditions.py
    ├── 5_🚘_Vehicle_Intelligence.py
    ├── 6_👥_Casualty_Analysis.py
    ├── 7_📈_Insights.py
    ├── 8_🎯_Recommendations.py
    └── 9_📘_Analytical_Overview.py
```

> **Note on page order:** Streamlit builds the sidebar directly from the numeric prefixes in `pages/`, in order. The numbering above puts **Time Intelligence right after Location** (where → when), then Weather/Vehicle (why), then Casualty (outcome), then Insights/Recommendations (so what → action) — matching the narrative your dashboard is meant to tell. Double-check your actual filenames match this order; if Time Intelligence is still numbered after Weather/Vehicle/Casualty in your repo, that's the one thing worth renaming before you publish.

---

## How to run

```
pip install -r requirements.txt
streamlit run Home.py
```

The app opens at `http://localhost:8501`. Streamlit auto-builds the sidebar navigation menu from the `pages/` folder — just click between pages.

The dataset is already bundled in `data/`, so it runs out of the box. To analyze a different file, use the "Load dataset" uploader in the sidebar (any page) — it applies across the whole app for that session.

---

## Tech Stack

Python · Pandas · Plotly · Streamlit

---

## Design

- Dark, BI-style theme (Power-BI-like palette) via `utils.inject_global_css()`.
- KPI cards: Total Accidents, Total Casualties, Serious Casualties, Fatal Casualties, Total Vehicles Involved — on the Executive Dashboard.
- Sidebar filters (Year, State, Weather, Severity, Road Type) persist across every page via `st.session_state`, so switching pages doesn't reset your selection.
- Download filtered data as CSV on the Executive Dashboard.
- Every chart and insight is computed live from the filtered data — nothing is hardcoded.

---

## Data Source

Real-world dataset sourced from Kaggle — not synthetic. 20,000 records spanning Jan 2022–Apr 2025 across 7 states and 8 cities.

## Honest scope notes

The bundled dataset (`indian_roads_dataset.xlsx`) has 16 fields: city, state, latitude/longitude, date, time, day_of_week, road_type, traffic_signal, weather, visibility, traffic_density, cause, accident_severity, vehicles_involved, casualties.

It does not include: district (only city/state), individual vehicle type/age (only a `vehicles_involved` count per accident), or driver-level fields (gender, age, pedestrian/casualty class). Pages 4 and 5 were adapted to analyze what the data actually supports — vehicles-involved patterns and aggregate casualty patterns — with a note explaining the substitution, rather than fabricating fields that don't exist in the source data. If you get an extended dataset with those fields later, those two pages are the ones to extend first.

---

## Analytical Overview

The final page is a methodology appendix — it lays out what the underlying analysis actually covers, in order: Business Understanding, Dataset Understanding, Location Intelligence, Time Intelligence, Environmental & Severity Intelligence, Relationship Analysis, and Composite Risk Intelligence (state scoring and ranking). It's meant to be read last, for anyone who wants to see how the dashboard's conclusions were derived rather than just the conclusions themselves.

---

## Deploying

Push this folder to GitHub (including `data/`) and deploy for free on [Streamlit Community Cloud](https://streamlit.io/cloud), pointing it at `Home.py`. It builds automatically from `requirements.txt`.

---

## Author

Niyati — DAV Institute of Engineering and Technology

## License

MIT