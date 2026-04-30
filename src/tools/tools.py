from datetime import datetime
from typing import Annotated


def get_weekday(date_string: Annotated[str, "Format: YYYY-MM-DD"]) -> str:
    """Returns the weekday name for a given date."""
    return datetime.strptime(date_string, "%Y-%m-%d").strftime("%A")


def get_weather(city: Annotated[str, "City name"]) -> str:
    """Returns simplified weather info."""
    return f"Weather in {city}: ☀️ 22°C"
