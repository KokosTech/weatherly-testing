import os
import requests
from weather_app.exceptions import CityDoesNotExistException

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")


class WeatherAPI:
    @staticmethod
    def fetch_current_weather(city_name):
        current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
        current_weather = requests.get(current_weather_url).json()

        if current_weather['cod'] == 200:
            return current_weather
        else:
            raise CityDoesNotExistException

    @staticmethod
    def fetch_5days_forecast(lat, lon):
        daily_forecast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        daily_forecast = requests.get(daily_forecast_url).json()
        return daily_forecast
