import requests
from typing import Optional

from src.weather_app.models.weather_data import WeatherData
from src.weather_app.services.geocoding import GeocodingError, NetworkError


class WeatherAPIError(Exception):
    """Raised when weather API fails."""

    pass


def get_current_weather(
    lat: float, lon: float, location_name: str = "Unknown"
) -> WeatherData:
    """
    Fetch current weather from Open-Meteo API.
    Uses Streamlit's cache_data for caching.
    """
    if not -90 <= lat <= 90:
        raise WeatherAPIError("Latitude must be between -90 and 90")
    if not -180 <= lon <= 180:
        raise WeatherAPIError("Longitude must be between -180 and 180")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m",
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Network error while fetching weather: {e}")

    data = response.json()

    if "current" not in data:
        raise WeatherAPIError("Invalid response from weather API")

    current = data["current"]

    return WeatherData(
        temperature_c=current["temperature_2m"],
        humidity=current["relative_humidity_2m"],
        wind_speed=current["wind_speed_10m"],
        wind_direction=current["wind_direction_10m"],
        weather_code=current["weather_code"],
        location_name=location_name,
        latitude=lat,
        longitude=lon,
    )


def get_cached_weather(
    lat: float, lon: float, location_name: str = "Unknown", ttl: int = 300
):
    """
    Get weather with caching wrapper.
    Note: This uses Streamlit's cache_data - must be called within a Streamlit app.
    """
    import streamlit as st

    @st.cache_data(ttl=ttl)
    def _fetch_weather(lat: float, lon: float, location_name: str) -> WeatherData:
        return get_current_weather(lat, lon, location_name)

    return _fetch_weather(lat, lon, location_name)
