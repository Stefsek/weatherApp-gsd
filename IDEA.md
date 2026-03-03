# Modular Weather App with Streamlit

## Tech Stack

- **Framework:** Streamlit (Python web framework)
- **Package Manager:** UV (`uv add` for all packages)
- **Python:** 3.13.5
- **APIs:** Open-Meteo (geocoding + weather)

## Features

- Search any city for real-time weather
- Toggle between Celsius / Fahrenheit
- Display: temperature, condition, humidity, wind speed, wind direction
- Interactive map with city marker
- Dark theme with gradient design

---

## Design

**Keep these colors exact:**

| Element        | Value                          |
|----------------|-------------------------------|
| Background     | `#0a0a0f` → `#12121a` gradient |
| Cards          | `#1a1a24` → `#1e1e2a`, border `#2a2a3a` |
| Title          | `#00d4ff` → `#7c3aed` gradient text |
| Primary text   | `#ffffff`                      |
| Secondary      | `#9ca3af`                      |
| Accent         | `#5eead4`                      |

**Layout (400px max-width, centered):**

1. **Header** — "☁️ Weather" with gradient
2. **Search row** — City input (75%) + Unit toggle (25%)
3. **Weather card** — City name, large temp, condition (all centered)
4. **Metrics grid** — 3 equal columns: Humidity | Wind | Direction
   - ⚠️ CRITICAL: Use CSS Grid with `repeat(3, 1fr)` and `align-items: stretch`
   - All cards MUST be same height and perfectly aligned
5. **Map** — 300px height, dark theme
6. **Footer** — "Open-Meteo API"

---

## Project Structure

```
weather_app/
├── app.py                      # Main Streamlit entry point
├── config.py                   # API URLs
├── services/
│   ├── geocoding.py            # API: get coordinates
│   └── weather.py              # API: get weather data
├── models/
│   └── weather_data.py         # Data classes
├── utils/
│   ├── converters.py           # Temperature conversion
│   └── formatters.py           # Weather codes, wind direction
└── styles/
    └── theme.py                # Colors, styles
```

**Note:** Streamlit uses a simpler architecture - no separate state file needed. Use `st.session_state` for reactivity.

---

## Key Functions

### Wind Direction
```python
directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
              "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
index = round(degrees / 22.5) % 16
```

### Weather Codes
| Code    | Condition     |
|---------|--------------|
| 0       | Clear sky    |
| 1       | Mainly clear |
| 2       | Partly cloudy|
| 3       | Overcast     |
| 51–55   | Drizzle      |
| 61–65   | Rain         |
| 71–75   | Snow         |
| 95–99   | Thunderstorm |

### Temperature Conversion
```python
fahrenheit = (celsius * 9/5) + 32
```

---

## API Endpoints

- **Geocoding:** `https://geocoding-api.open-meteo.com/v1/search`
- **Weather:** `https://api.open-meteo.com/v1/forecast`

---

## Requirements

- Type hints everywhere
- Proper error handling (city not found, API errors)
- Separation of concerns (services / utils / components)
- Streamlit session state for reactivity
- Perfect alignment of metric cards
- UV package management only (no pip)

---

## Setup Commands

```bash
uv init weather_app
cd weather_app
uv add streamlit requests
uv run streamlit run app.py
```
