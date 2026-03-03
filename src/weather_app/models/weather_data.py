from dataclasses import dataclass
from typing import Optional


@dataclass
class GeocodingResult:
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("name must be a non-empty string")
        if (
            not isinstance(self.latitude, (int, float))
            or not -90 <= self.latitude <= 90
        ):
            raise ValueError("latitude must be between -90 and 90")
        if (
            not isinstance(self.longitude, (int, float))
            or not -180 <= self.longitude <= 180
        ):
            raise ValueError("longitude must be between -180 and 180")


@dataclass
class WeatherData:
    temperature_c: float
    humidity: float
    wind_speed: float
    wind_direction: int
    weather_code: int
    location_name: str
    latitude: float
    longitude: float

    def __post_init__(self):
        if not isinstance(self.temperature_c, (int, float)):
            raise ValueError("temperature_c must be a number")
        if not isinstance(self.humidity, (int, float)) or not 0 <= self.humidity <= 100:
            raise ValueError("humidity must be between 0 and 100")
        if not isinstance(self.wind_speed, (int, float)) or self.wind_speed < 0:
            raise ValueError("wind_speed must be non-negative")
        if (
            not isinstance(self.wind_direction, int)
            or not 0 <= self.wind_direction <= 360
        ):
            raise ValueError("wind_direction must be between 0 and 360")
        if not isinstance(self.weather_code, int) or not 0 <= self.weather_code <= 99:
            raise ValueError("weather_code must be between 0 and 99")
        if not isinstance(self.location_name, str) or not self.location_name:
            raise ValueError("location_name must be a non-empty string")
        if (
            not isinstance(self.latitude, (int, float))
            or not -90 <= self.latitude <= 90
        ):
            raise ValueError("latitude must be between -90 and 90")
        if (
            not isinstance(self.longitude, (int, float))
            or not -180 <= self.longitude <= 180
        ):
            raise ValueError("longitude must be between -180 and 180")
