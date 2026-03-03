# Retrospective

## Milestone: v1.0 — MVP

**Shipped:** 2026-03-03
**Phases:** 2 | **Plans:** 5

### What Was Built

- Foundation layer: type-safe data models, Open-Meteo API services, WMO code mapping, caching
- Streamlit UI: city search, C/F toggle, weather metrics, error handling
- Visual polish: dark gradient theme, 3-column metrics cards, interactive Folium map

### What Worked

- **Open-Meteo API** — free, no key, reliable. Zero setup friction.
- **Dataclass pattern** — `__post_init__` validation caught bugs early
- **Streamlit caching** (`@cache_data`) — seamless, no extra work
- **Modular structure** (`services/`, `models/`, `utils/`) — clean separation made Phase 2 edits easy
- **CSS injection via `st.markdown`** — practical workaround for Streamlit's theming limits

### What Was Inefficient

- Layout width was set to 400px max (matching the design spec) but this made the app look mobile-narrow on desktop — required a second pass to remove the constraint
- Phase 2 initial summaries referenced old CSS values (`.centered-container`, `rgba(255,255,255,0.05)`) that were later overhauled; planning docs needed re-syncing

### Patterns Established

- CSS injection pattern: `st.markdown('<style>...</style>', unsafe_allow_html=True)` in `main()` before any components
- Iframe CSS injection: `m.get_root().html.add_child(folium.Element('<style>...</style>'))` for Folium map internals
- Spacer pattern: `st.markdown('<div style="margin-top: Xrem;"></div>', unsafe_allow_html=True)` for inter-component spacing

### Key Lessons

1. **Design specs ≠ desktop reality** — A 400px max-width spec from a design doc is meant for the content card, not the Streamlit block container; always test at actual viewport width
2. **Streamlit CSS scoping** — Streamlit CSS can't reach inside Folium iframes; inject CSS into the folium map object directly
3. **Planning doc drift** — When doing CSS overhauls, planning docs (VERIFICATION.md, CONTEXT.md) quickly go stale; update them in the same pass

### Cost Observations

- Sessions: 1 (single-session build)
- Total execution: ~75 min (5 plans × avg ~15 min including post-session polish)
- Notable: Post-phase polish (layout width fix, attribution hide, color tweaks) added ~20% extra time on top of planned execution

---

## Cross-Milestone Trends

| Milestone | Phases | Plans | LOC | Velocity |
|-----------|--------|-------|-----|----------|
| v1.0 MVP  | 2      | 5     | 571 | ~75 min  |
