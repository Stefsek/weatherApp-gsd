# Architecture Research

**Domain:** Streamlit Weather Application
**Researched:** 2026-03-03
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     UI Layer (Streamlit)                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ app.py      │  │ components/ │  │ st.session_state    │ │
│  │ (entry)     │  │ (display)   │  │ (reactive state)    │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         │                │                     │            │
├─────────┴────────────────┴─────────────────────┴────────────┤
│                    Service Layer                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────────────┐  │
│  │ services/geocoding.py│  │ services/weather.py        │  │
│  │ (API: coordinates)   │  │ (API: weather data)        │  │
│  └─────────────────────┘  └─────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    Utility Layer                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐                │
│  │ utils/converters│  │ utils/formatters │                │
│  │ (temp units)    │  │ (display format) │                │
│  └─────────────────┘  └─────────────────┘                │
├─────────────────────────────────────────────────────────────┤
│                    Models Layer                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────────────┐  │
│  │ models/weather_data │  │ config.py                  │  │
│  │ (data classes)      │  │ (API URLs, constants)      │  │
│  └─────────────────────┘  └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| `app.py` | Main entry point, UI layout, user interaction | Streamlit script, runs top-to-bottom on each rerun |
| `services/geocoding.py` | Fetch city coordinates from Open-Meteo Geocoding API | `@st.cache_data` decorated function |
| `services/weather.py` | Fetch weather data from Open-Meteo Weather API | `@st.cache_data` decorated function with TTL |
| `models/weather_data.py` | Data classes for type safety | Python dataclasses with type hints |
| `utils/converters.py` | Temperature unit conversion | Pure functions, no state |
| `utils/formatters.py` | Format weather codes, wind direction | Pure functions, no state |
| `styles/theme.py` | Dark theme colors and CSS injection | Streamlit's `st.markdown` with `<style>` |
| `config.py` | API endpoints and constants | Module-level constants |

## Recommended Project Structure

```
weather_app/
├── app.py                      # Main Streamlit entry point
├── config.py                   # API URLs, constants
├── services/
│   ├── geocoding.py            # Geocoding API client
│   └── weather.py              # Weather API client
├── models/
│   └── weather_data.py         # Data classes (WeatherData, GeoLocation)
├── utils/
│   ├── converters.py           # Temperature conversion (C ↔ F)
│   └── formatters.py           # Weather code → text, wind direction
└── styles/
    └── theme.py                # Color constants, CSS injection
```

### Structure Rationale

- **`services/`:** API calls isolated here. Easy to add caching, swap APIs, or add retry logic without touching UI code.
- **`models/`:** Data classes provide type safety. Separate from services so models can be used independently.
- **`utils/`:** Pure functions with no side effects. Easy to test in isolation.
- **`styles/`:** Theme and styling separated from logic. Dark mode colors defined once, reused throughout.
- **`app.py`:** Thin orchestration layer. Calls services, passes data to display functions. Minimal business logic.

## Architectural Patterns

### Pattern 1: Script Rerun Model

**What:** Streamlit executes the entire script from top to bottom on every user interaction. No explicit event handlers needed.

**When to use:** Any Streamlit app. This is the fundamental execution model.

**Trade-offs:**
- Pro: Simple mental model, easy to debug
- Pro: Fast development loop
- Con: Must be careful about expensive operations re-running
- Con: No fine-grained reactivity (whole app rerenders)

**Example:**
```python
import streamlit as st

# This runs on every interaction
city = st.text_input("City")
if city:
    weather = fetch_weather(city)  # Runs every time
    st.write(weather)
```

### Pattern 2: Session State for Reactivity

**What:** Use `st.session_state` to persist values across reruns. Required for any state that must survive a script rerun.

**When to use:** When you need to remember user choices, cache API responses, or maintain any state between interactions.

**Trade-offs:**
- Pro: Simple API
- Con: Adds complexity — must initialize state before use
- Con: Not persisted across tabs/sessions

**Example:**
```python
import streamlit as st

if 'unit' not in st.session_state:
    st.session_state.unit = 'celsius'

# Widget with key syncs with session_state
unit = st.segmented_control("Unit", ["Celsius", "Fahrenheit"], key="unit")
```

### Pattern 3: Caching with `@st.cache_data`

**What:** Decorator that caches function results. Avoids re-running expensive operations (API calls, data transformations).

**When to use:** For any function that fetches data from APIs, loads files, or performs expensive computations.

**Trade-offs:**
- Pro: Dramatic performance improvement
- Pro: Simple to add (one decorator)
- Con: Must use hashable parameters
- Con: Can return stale data (use `ttl` parameter)

**Example:**
```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_weather(lat: float, lon: float) -> dict:
    response = requests.get(WEATHER_URL, params={...})
    return response.json()
```

### Pattern 4: Widgets as Variables

**What:** Streamlit widgets return their value directly. No need for callbacks or event handlers.

**When to use:** Always. This is the primary way to get user input.

**Trade-offs:**
- Pro: Very intuitive
- Con: Value resets on rerun unless stored in session_state

**Example:**
```python
city = st.text_input("City")  # Returns string directly
unit = st.toggle("Fahrenheit")  # Returns boolean
```

## Data Flow

### Request Flow

```
[User Types City Name]
        ↓
[app.py: st.text_input()]
        ↓
[services/geocoding.py: get_coordinates()]
        ↓ (API call, cached)
[Open-Meteo Geocoding API]
        ↓ (returns lat/lon)
[services/weather.py: get_weather()]
        ↓ (API call, cached)
[Open-Meteo Weather API]
        ↓ (returns JSON)
[models/weather_data.py: WeatherData()]
        ↓ (parsed to dataclass)
[utils/formatters.py: format_weather_code()]
        ↓ (human-readable text)
[app.py: st.metric(), st.map()]
        ↓
[User Sees Weather Display]
```

### State Management

```
[st.session_state]
    ├── unit: str ("celsius" | "fahrenheit")
    ├── last_city: str (for caching/optimization)
    └── weather_cache: dict (optional manual cache)
```

### Key Data Flows

1. **City Search Flow:** User enters city → geocoding service returns coordinates → weather service fetches data → UI displays results
2. **Unit Toggle Flow:** User toggles unit → session_state updates → app reruns → converters transform displayed values

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-1k users | Single Streamlit instance, no changes needed. Open-Meteo API rate limits are generous for personal apps. |
| 1k-100k users | Add `@st.cache_data` with appropriate TTL to API calls. Consider Redis for session state if deploying to multiple instances. |
| 100k+ users | Consider moving API aggregation to a separate backend service. Streamlit becomes the display layer only. |

### Scaling Priorities

1. **First bottleneck:** API response time. Fix: Aggressive caching with `ttl` parameter on weather API calls.
2. **Second bottleneck:** Session state in multi-instance deployment. Fix: Use external state store (Redis) or sticky sessions.

## Anti-Patterns

### Anti-Pattern 1: Putting API Calls in Main Script

**What people do:** Writing `requests.get()` directly in `app.py` without caching.

**Why it's wrong:** Every widget interaction triggers a new API call. Slow UX, potential rate limiting.

**Do this instead:** Move API calls to `services/` with `@st.cache_data` decorator.

### Anti-Pattern 2: Forgetting Session State Initialization

**What people do:** Using `st.session_state.some_var` without checking if it exists first.

**Why it's wrong:** Raises `KeyError` on first run when the key doesn't exist yet.

**Do this instead:**
```python
if 'unit' not in st.session_state:
    st.session_state.unit = 'celsius'
```

### Anti-Pattern 3: Complex Callbacks for Simple State

**What people do:** Using `on_change` callbacks when direct widget assignment would work.

**Why it's wrong:** Callbacks add complexity. Widgets with `key` parameter auto-sync to session state.

**Do this instead:**
```python
# Instead of callback
st.toggle("Fahrenheit", key="unit")

# Use directly
if st.session_state.unit == "fahrenheit":
    display_fahrenheit(temp)
```

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Open-Meteo Geocoding | `requests.get()` + `@st.cache_data` | No API key needed. Cache by city name. |
| Open-Meteo Weather | `requests.get()` + `@st.cache_data(ttl=300)` | 5-minute TTL for real-time feel. Cache by coordinates. |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| app.py ↔ services | Direct function calls | Services return data, app displays it |
| app.py ↔ utils | Import and call | Pure functions, no state shared |
| app.py ↔ models | Import dataclass | Type hints throughout |

## Sources

- [Streamlit Basic Concepts](https://docs.streamlit.io/get-started/fundamentals/main-concepts) — HIGH confidence
- [Streamlit Session State](https://docs.streamlit.io/develop/concepts/architecture/session-state) — HIGH confidence
- [Streamlit Caching](https://docs.streamlit.io/develop/concepts/architecture/caching) — HIGH confidence

---
*Architecture research for: Weather App (Streamlit)*
*Researched: 2026-03-03*
