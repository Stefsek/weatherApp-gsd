# Stack Research

**Domain:** Weather App with Streamlit
**Researched:** 2026-03-03
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Streamlit | Latest (1.40+) | Web UI framework | Industry standard for data apps; minimal boilerplate; built-in state management; rapid prototyping. Active development by Snowflake. |
| Python | 3.13.5 | Runtime | Project requirement; modern Python with full type hint support |
| Open-Meteo API | v1 | Weather data | Free, no API key required; global coverage; multiple weather models; WMO standard codes |
| UV | Latest | Package manager | Project requirement; faster than pip; better dependency resolution |
| requests | 2.33+ | HTTP client | De facto standard for Python HTTP; synchronous simple for this use case |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| streamlit-folium | latest | Interactive maps | When you need custom map markers, dark theme maps, or more control than st.map() |
| folium | latest | Map rendering | Required by streamlit-folium for generating map objects |
| pydantic | 2.x | Data validation | When you need robust type validation for API responses |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| Streamlit CLI | Local dev server | `uv run streamlit run app.py` |
| Browser preview | Hot reload | Streamlit auto-refreshes on file save |
| Python type hints | Type safety | Required by project; use `typing` module |

## Installation

```bash
# Core (using UV as package manager - project requirement)
uv add streamlit requests folium streamlit-folium pydantic

# Run development
uv run streamlit run app.py

# Or use the CLI directly after installation
streamlit run app.py
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| requests | httpx | When you need async HTTP (e.g., multiple simultaneous API calls) |
| Open-Meteo | WeatherAPI.com | When you need premium features or more detailed forecasts (requires paid tier) |
| Open-Meteo | OpenWeatherMap | When you need US-centric data or prefer their response format |
| streamlit-folium | st.map (built-in) | Simple scatter plots on maps; st.map is lighter weight but less customizable |
| streamlit-folium | pydeck | 3D/map visualizations; more complex but powerful |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| pip (unless required) | Project constraint specifies UV | UV for faster installs and better lock files |
| aiohttp | Overkill for single API calls; adds complexity | requests (sync) is sufficient |
| weather-sdk libraries | Often outdated; Open-Meteo has simple REST API | Direct API calls with requests |
| Multiple weather APIs initially | Adds complexity; single API MVP is faster | Start with Open-Meteo only |
| Flask/Django | Too heavy for simple weather display | Streamlit is purpose-built for data apps |

## Stack Patterns by Variant

**If you need forecasts (future enhancement):**
- Use Open-Meteo `forecast_days` parameter
- Already supported by current API choice

**If you need multiple locations saved:**
- Add SQLite or JSON file storage
- Keep simple initially, add persistence later

**If you need weather alerts:**
- Open-Meteo doesn't provide alerts natively
- Would need secondary API (NWS API, etc.)

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| streamlit | Python 3.9+ | Current docs specify 3.9+ |
| requests | Python 3.9+ | Verified in docs |
| folium | Python 3.x | Requires Leaflet.js (bundled) |
| streamlit-folium | Streamlit 1.10+ | Check compatibility with Streamlit version |
| pydantic | Python 3.9+ | v2.x is current |

## Sources

- Streamlit API Reference — https://docs.streamlit.io/library/api-reference — Verified current capabilities, widgets, and chart elements
- Open-Meteo Weather API Docs — https://open-meteo.com/en/docs — Verified current weather variables, WMO codes, and free tier details
- Requests Library — https://requests.readthedocs.io/en/latest/ — Version 2.33.x confirmed, Python 3.9+ support
- Streamlit Installation — https://docs.streamlit.io/get-started/installation — Current installation methods verified
- Streamlit Folium Component — https://github.com/randyzwitch/streamlit-folium — Community-maintained, enables dark theme maps

---

*Stack research for: Weather App with Streamlit*
*Researched: 2026-03-03*
