import os
import requests
from jsonschema import validate
from weather_app.exceptions import CityDoesNotExistException
from weather_app.schemas import CURRENT_WEATHER_SCHEMA, DAILY_FORECAST_SCHEMA
from weather_app.constants import REQUEST_TIMEOUT as REQU

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")


class WeatherAPI:
    @staticmethod
    def fetch_current_weather(city_name):
        current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
        current_weather = requests.get(current_weather_url, timeout=REQU).json()

        if current_weather["cod"] == 200:
            validate(current_weather, CURRENT_WEATHER_SCHEMA)
            return current_weather

        raise CityDoesNotExistException

    @staticmethod
    def fetch_5days_forecast(lat, lon):
        daily_forecast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        daily_forecast = requests.get(daily_forecast_url, timeout=REQU).json()

        validate(daily_forecast, DAILY_FORECAST_SCHEMA)

        return daily_forecast
