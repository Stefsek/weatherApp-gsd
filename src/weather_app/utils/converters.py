def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def format_temperature(celsius: float, unit: str = "C") -> str:
    """Format temperature with degree symbol."""
    if unit.upper() == "F":
        temp = celsius_to_fahrenheit(celsius)
        return f"{temp:.1f}°F"
    return f"{celsius:.1f}°C"
