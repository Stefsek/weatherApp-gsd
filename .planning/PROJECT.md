# Weather App

## What This Is

A modular weather application built with Streamlit that lets users search any city and instantly view real-time weather: temperature (C/F toggle), conditions, humidity, wind speed & direction, and an interactive dark-themed map with a city marker.

## Core Value

Users can quickly search for any city and get accurate, real-time weather information with a beautiful, responsive interface.

## Current State (v1.0)

- **Status:** Shipped — all 19 v1 requirements complete
- **Entry point:** `main.py` → `uv run streamlit run main.py`
- **Python LOC:** 571 | **Tech:** Streamlit 1.40+, Folium, Open-Meteo API
- **Theme:** Dark gradient (`#0a0a0f → #12121a`) via CSS + config.toml
- **Key files:** `main.py`, `.streamlit/config.toml`, `src/weather_app/`

## Requirements

### Validated

- ✓ User can search for any city by name — v1.0
- ✓ Display current temperature in chosen unit (Celsius/Fahrenheit) — v1.0
- ✓ Show weather condition (clear, cloudy, rain, etc.) — v1.0
- ✓ Display humidity percentage — v1.0
- ✓ Show wind speed and direction (cardinal) — v1.0
- ✓ Error handling for city not found and API/network failures — v1.0
- ✓ Interactive map with city marker — v1.0
- ✓ Dark theme with gradient design — v1.0

### Active

*(None — start `/gsd:new-milestone` to define v1.1 requirements)*

### Out of Scope

- Weather forecasts (future enhancement)
- Multiple saved favorite locations
- Weather alerts/notifications
- Mobile native app
- Multiple API providers

## Context

- **Tech Stack:** Streamlit (Python), Open-Meteo API (free, no key required), Folium + streamlit-folium
- **Package Manager:** UV
- **Python Version:** 3.13.5
- **Project Structure:** Modular — `src/weather_app/` with `services/`, `models/`, `utils/`

## Constraints

- **API:** Open-Meteo (free, no authentication required)
- **Quality:** Type hints everywhere, proper error handling, separation of concerns
- **Layout:** Streamlit default container width (removed 400px cap — too narrow on desktop)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Streamlit framework | Fastest path to working web UI for data app | ✓ Good |
| Open-Meteo API | Free, no API key, good global coverage | ✓ Good |
| UV package manager | Modern, fast Python package manager | ✓ Good |
| Dataclasses + `__post_init__` validation | Type safety without Pydantic overhead | ✓ Good |
| `@cache_data` 300s TTL | Prevent redundant API calls on rerenders | ✓ Good |
| CartoDB dark_matter tiles | Matches dark theme aesthetic | ✓ Good |
| CSS injection for gradient bg + `.block-container` | config.toml doesn't support gradients or centering | ✓ Good |
| `folium.Element` to hide Leaflet attribution | Attribution lives in iframe, Streamlit CSS can't reach it | ✓ Good |
| Removed 400px max-width | 400px was too narrow on desktop — content squeezed, C/F buttons stacked | ✓ Good |
| Condition text color `#00d4ff` (cyan) | Purple was inconsistent; cyan matches the title/cloud accent | ✓ Good |

---
*Last updated: 2026-03-03 after v1.0 milestone*
