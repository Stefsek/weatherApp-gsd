# Pitfalls Research

**Domain:** Streamlit Weather Application
**Researched:** 2026-03-03
**Confidence:** MEDIUM

## Critical Pitfalls

### Pitfall 1: Missing API Caching Causes Rate Limiting

**What goes wrong:**
Every keystroke or widget interaction triggers new API calls to Open-Meteo. Without caching, the app feels slow and may hit rate limits.

**Why it happens:**
Streamlit reruns the entire script on each interaction. Developers new to Streamlit forget that `requests.get()` in the main script executes on every rerun.

**How to avoid:**
Use `@st.cache_data` decorator on all API calls with appropriate TTL:
```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_weather(lat: float, lon: float) -> dict:
    response = requests.get(WEATHER_URL, params={...})
    return response.json()
```

**Warning signs:**
- App feels sluggish on every interaction
- Console shows repeated API calls
- Open-Meteo returns 429 errors

**Phase to address:**
Phase 2: Core Features — Implement caching on API services

---

### Pitfall 2: Session State Not Initialized

**What goes wrong:**
`KeyError` when accessing `st.session_state` variables that don't exist on first run.

**Why it happens:**
Streamlit resets session state on page refresh. Code that assumes state exists will crash on fresh load.

**How to avoid:**
Always initialize state before use:
```python
if 'unit' not in st.session_state:
    st.session_state.unit = 'celsius_city' not in'
if 'last st.session_state:
    st.session_state.last_city = None
```

**Warning signs:**
- `KeyError: 'unit'` in console on page refresh
- App crashes after browser refresh

**Phase to address:**
Phase 1: Project Setup — Add state initialization to app entry point

---

### Pitfall 3: Weather Code Mapping Errors

**What goes wrong:**
Users see raw WMO weather codes (0, 1, 2, 61) instead of human-readable conditions ("Clear sky", "Rain").

**Why it happens:**
Open-Meteo returns numeric codes. Developers forget to map these to text, or only map a subset of codes.

**How to avoid:**
Create complete weather code mapping in `utils/formatters.py`:
```python
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    # ... complete list from WMO standards
}
```

**Warning signs:**
- Numbers displayed instead of weather conditions
- Only some weather conditions display correctly
- Code appears in logs or UI

**Phase to address:**
Phase 1: Project Setup — Implement formatters with complete WMO code mapping

---

### Pitfall 4: Geocoding Failure Breaks Entire App

**What goes wrong:**
Typing a city name that doesn't exist or has API issues causes unhandled exception. App crashes with no graceful message.

**Why it happens:**
No error handling around geocoding API response. Assumes API always returns valid data.

**How to avoid:**
Wrap API calls in try/except with specific error handling:
```python
def get_coordinates(city: str) -> GeoLocation | None:
    try:
        response = requests.get(GEOCODING_URL, params={"name": city}, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data.get("results"):
            return None  # City not found
        return GeoLocation(**data["results"][0])
    except requests.RequestException:
        st.error("Unable to find city. Please try again.")
        return None
```

**Warning signs:**
- App crashes on invalid city input
- No feedback when city not found
- Generic Python errors visible to users

**Phase to address:**
Phase 1: Project Setup — Add error handling to all service layer functions

---

### Pitfall 5: Widget Key Collision

**What goes wrong:**
Multiple widgets with same `key` or using widget values without proper session_state sync causes unexpected behavior.

**Why it happens:**
Streamlit widgets with `key` parameter auto-sync to session_state. Reusing keys or not understanding the sync causes stale values.

**How to avoid:**
Use unique keys and understand auto-sync:
```python
# Correct: key syncs to session_state automatically
unit_toggle = st.toggle("°F", key="unit_toggle")
# Access via session_state
if st.session_state.unit_toggle:
    display_fahrenheit()
```

**Warning signs:**
- Unit toggle doesn't update display
- Values seem to persist incorrectly
- State changes don't reflect in UI

**Phase to address:**
Phase 2: Core Features — Widget implementation

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcoding API responses | Faster initial dev | Can't handle API changes, no error handling | Never |
| Skipping type hints | Less typing | Runtime errors, hard to debug | Never |
| Single huge app.py | Simpler file structure | Hard to maintain, test, or extend | Only for <50 line prototypes |
| No caching | Simpler code | Slow UX, rate limit issues | Never |
| Skipping models/dataclasses | Faster initial setup | No type safety, brittle code | Never |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Open-Meteo Geocoding | Not checking if results array is empty | Verify `data.get("results")` before indexing |
| Open-Meteo Weather | Requesting unused data fields | Only request needed parameters to reduce payload |
| Streamlit + Maps | Using st.map with custom markers | Use streamlit-folium for custom dark theme maps |
| Temperature units | Not converting before display | Apply conversion in display layer, keep source as Celsius |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| No caching on API calls | Slow on every interaction | Add `@st.cache_data` to all service functions | Immediately |
| Caching without TTL | Stale data shown forever | Use `ttl` parameter: `@st.cache_data(ttl=300)` | After 5+ minutes |
| Large response payloads | Slow initial load | Request only needed fields from API | With slow connections |
| Unnecessary reruns | Everything re-runs on any input | Use `st.fragment` (Streamlit 1.33+) for partial rerenders | With complex layouts |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Exposing API keys in code | Unauthorized API usage, quota exhaustion | Use environment variables if keys required (Open-Meteo doesn't need keys) |
| No input sanitization on city names | Potential injection in logging/monitoring | Sanitize user input before API calls |
| Storing sensitive session data | Data exposure in server logs | Avoid storing sensitive data in session_state |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|------------------|
| No loading states | App appears frozen during API calls | Show `st.spinner()` during fetches |
| No feedback for empty search | User doesn't know if search worked | Show "Enter a city name" message |
| Weather without location context | User unsure which city's weather shown | Always display city name prominently |
| Map without fallback | Map fails to load in some environments | Show coordinates as text backup |
| No unit preference persistence | User must toggle unit every visit | Store preference in session_state |

---

## "Looks Done But Isn't" Checklist

- [ ] **Weather display:** Often missing wind direction ( compass) — verify N/S/E/W displays
- [ ] **Map:** Often broken with custom themes — verify map loads with dark tiles
- [ ] **Error handling:** Often missing "city not found" — verify graceful message
- [ ] **Unit toggle:** Often doesn't update displayed temperature — verify conversion works
- [ ] **Caching:** Often missing TTL — verify data freshness with `ttl` parameter

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Missing caching | LOW | Add `@st.cache_data(ttl=300)` to API functions |
| KeyError on session_state | LOW | Add initialization at app start |
| API failure crashes | MEDIUM | Wrap in try/except, add error UI |
| Weather code numbers shown | LOW | Complete WMO code mapping in formatters |
| Map theme broken | MEDIUM | Check streamlit-folium tile URL configuration |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Missing API caching | Phase 2: Core Features | Test interaction responsiveness |
| Session state not initialized | Phase 1: Project Setup | Refresh page, verify no crashes |
| Weather code mapping errors | Phase 1: Project Setup | Test multiple weather conditions |
| Geocoding failure breaks app | Phase 1: Project Setup | Test invalid city input |
| Widget key collision | Phase 2: Core Features | Test unit toggle behavior |
| No loading states | Phase 2: Core Features | Test slow network conditions |

---

## Sources

- Streamlit Caching Documentation — https://docs.streamlit.io/develop/concepts/architecture/caching — HIGH confidence
- Streamlit Session State — https://docs.streamlit.io/develop/concepts/architecture/session-state — HIGH confidence
- Open-Meteo Weather Codes — https://open-meteo.com/en/docs — WMO standard code reference
- Community discussions on Streamlit weather app issues — LOW confidence (general knowledge)

---

*Pitfalls research for: Streamlit Weather Application*
*Researched: 2026-03-03*
