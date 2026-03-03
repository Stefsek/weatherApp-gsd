# Phase 2: Visual Polish - Context

**Gathered:** 2026-03-03
**Updated:** 2026-03-03
**Status:** Implemented (patched 2026-03-03)

<domain>
## Phase Boundary

Apply visual polish to the weather app: dark theme with gradient design, centered 400px layout, 3-column metrics grid, main weather card, and interactive map with city marker. This phase focuses on UI/UX improvements only — core weather functionality from Phase 1 remains unchanged.

</domain>

<decisions>
## Implementation Decisions

### Color & Theme
- Dark theme applied via both `.streamlit/config.toml` AND CSS injection in `main.py`
- Background gradient: `linear-gradient(180deg, #0a0a0f 0%, #12121a 100%)` on `.stApp` via CSS
- `config.toml`: `backgroundColor="#0d0d14"`, `secondaryBackgroundColor="#1a1a24"`
- Title: "Weather" with cloud icon, blue-purple gradient (#00d4ff → #7c3aed)

### Layout Structure (Final)
1. **Title**: "☁️ Weather" centered at top with gradient
2. **Search row**: Search input (left, 4/5 width) + Temperature unit C/F toggle (right, 1/5 width)
3. **Main weather card**: City name, large temperature, condition (purple text); gradient bg with border
4. **Metrics row**: 3 equal cards — Humidity | Wind Speed | Direction; gradient bg with border
5. **Map**: Full container width (`use_container_width=True`), 250px height, dark theme tiles
6. **Footer**: "Open-Meteo API" centered at bottom

### Container Centering
- `.block-container` CSS override: `max-width: 400px !important; margin: 0 auto !important;`
- NOT using a `.centered-container` wrapper class

### C/F Toggle Styling
- `[data-testid="stSegmentedControl"] > div`: dark `#0e0e16` background, `#2a2a3a` border
- Active label: `1.5px solid #00d4ff` border, transparent background
- Inactive label: transparent border, transparent background

### Metrics Grid
- Grid layout: 3 equal columns
- Card 1: Humidity (e.g., "82%")
- Card 2: Wind speed only (e.g., "7.9 km/h") — NOT combined with direction
- Card 3: Wind direction only (e.g., "NE")
- Card styling: Subtle background, light shadow, rounded corners

### Map Integration
- Library: Streamlit-Folium
- Map tiles: CartoDB dark_matter (dark theme)
- City marker: Circle marker (cyan #00d4ff)
- Width: Full container width (400px)

### Spacing (inline spacer divs, `margin-top`)
- Weather card: `margin: 1rem 0` on the card div
- Before metrics row: `margin-top: 1rem` spacer div
- Before map: `margin-top: 2rem` spacer div (user increased from 1rem)
- Footer: `margin-top: 1rem`
- Container: `padding-top: 2rem`, `padding-bottom: 1rem` on `.block-container`

### Claude's Discretion
- Card padding, border-radius, shadow values
- Map zoom level (10) and height (250px)
- Font sizes for main display and metrics

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `WeatherData` model in `src/weather_app/models/weather_data.py` — already has latitude/longitude for map
- `search_city` returns geocoding result with latitude, longitude, and name
- Session state already manages temperature_unit preference
- `format_temperature`, `format_weather_code`, `format_wind_direction` utilities

### Established Patterns
- Streamlit for UI (Phase 1)
- Error handling via session state (Phase 1)
- Custom converters and formatters in utils/ (Phase 1)

### Integration Points
- Map displays after weather data is fetched (when `weather_data` is in session state)
- st_folium integrated into main.py after metrics display

</code_context>

<specifics>
## Specific Ideas

- User prefers Streamlit-native solutions over custom CSS where possible
- Lighter dark theme feels more modern and easier on eyes
- Map should feel cohesive with dark theme — dark tiles match app aesthetic
- Metrics cards should feel like distinct "tiles" with consistent height
- Main weather display should prominently show city, temp, and condition
- Wind speed and direction should be separate metrics (not combined)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-visual-polish*
*Context gathered: 2026-03-03*
*Layout finalized: 2026-03-03*
