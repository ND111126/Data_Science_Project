# 🚦 RoadScape — Safety Intelligence Platform

A resume-worthy, multi-page Streamlit BI dashboard analyzing 20,000+ Indian
road accident records across 8 cities and 7 states.

## Project Structure

```
roadscape_dashboard/
├── app.py                                  # Page 1 — Executive Dashboard (entry point)
├── utils.py                                # Shared theme, data loading, filters, KPI cards
├── requirements.txt
├── data/
│   └── indian_roads_dataset21.xlsx         # Bundled dataset
├── assets/
│   └── logo.svg
└── pages/
    ├── 2_📍_Location_Intelligence.py
    ├── 3_🌦️_Weather_Road_Conditions.py
    ├── 4_🚘_Vehicle_Intelligence.py
    ├── 5_👥_Casualty_Analysis.py
    ├── 6_⏰_Time_Intelligence.py
    ├── 7_📈_Insights.py
    └── 8_🎯_Recommendations.py
```

## How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`. Streamlit auto-builds the sidebar
navigation menu from the `pages/` folder — just click between pages.

The dataset is already bundled in `data/`, so it runs out of the box. To
analyze a different file, use the "Load dataset" uploader in the sidebar
(any page) — it applies across the whole app for that session.

## Design

- **Dark, BI-style theme** (Power-BI-like palette) via `utils.inject_global_css()`.
- **KPI cards**: Total Accidents, Total Casualties, Serious Casualties, Fatal
  Casualties, Total Vehicles Involved — on the Executive Dashboard.
- **Sidebar filters** (Year, State, Weather, Severity, Road Type) persist
  across every page via `st.session_state`, so switching pages doesn't reset
  your selection.
- **Download filtered data as CSV** on the Executive Dashboard.
- Every chart and insight is computed **live** from the filtered data —
  nothing is hardcoded.

## Honest scope notes

The bundled dataset (`indian_roads_dataset21.xlsx`) has 16 fields: city,
state, latitude/longitude, date, time, day_of_week, road_type,
traffic_signal, weather, visibility, traffic_density, cause,
accident_severity, vehicles_involved, casualties.

It does **not** include: district (only city/state), individual vehicle
type/age (only a `vehicles_involved` count per accident), or driver-level
fields (gender, age, pedestrian/casualty class). Pages 4 and 5 were adapted
to analyze what the data actually supports — vehicles-involved patterns and
aggregate casualty patterns — with a note explaining the substitution, rather
than fabricating fields that don't exist in the source data. If you get an
extended dataset with those fields later, those two pages are the ones to
extend first.

## Deploying

Push this folder to GitHub (including `data/`) and deploy for free on
[Streamlit Community Cloud](https://streamlit.io/cloud), pointing it at
`app.py`. It builds automatically from `requirements.txt`.
