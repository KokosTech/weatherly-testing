from datetime import datetime

import requests

WEATHER_API_KEY = "527183b7900188cd42cccab8cc903fd5"

def city_exists(city_name):
    current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
    current_weather = requests.get(current_weather_url).json()
    if current_weather['cod'] == 200:
        return True
    return False

class WeatherAPI:
    @staticmethod
    def fetch_current_weather(city_name):
        current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
        current_weather = requests.get(current_weather_url).json()
        return current_weather

    @staticmethod
    def fetch_5days_forecast(lat, lon):
        daily_forecast_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        daily_forecast = requests.get(daily_forecast_url).json()
        return daily_forecast

class CityWeather:
    def __init__(self, json):
        self.name = json['name']
        self.country = json['sys']['country']
        self.icon = json['weather'][0]['icon']
        self.description = json['weather'][0]['description'].title()
        self.temp = round(json['main']['temp'])
        self.high = round(json['main']['temp_max'])
        self.low = round(json['main']['temp_min'])
        self.humidity = json['main']['humidity']
        self.wind_speed = round(json['wind']['speed'])
        self.sunrise = datetime.utcfromtimestamp(json['sys']['sunrise']).strftime('%H:%M')
        self.sunset = datetime.utcfromtimestamp(json['sys']['sunset']).strftime('%H:%M')
        self.forecast = []

    def add_daily_forecast(self, json):
        for i in range(1, 6):
            day = json['daily'][i]
            self.forecast.append({
                'day': datetime.utcfromtimestamp(day['dt']).strftime('%a'),
                'date': datetime.utcfromtimestamp(day['dt']).strftime('%d/%m'),
                'icon': day['weather'][0]['icon'],
                'low': round(day['temp']['min']),
                'high': round(day['temp']['max']),
                'wind_speed': round(day['wind_speed']),
                'humidity': day['humidity']
            })

    @staticmethod
    def get_weather(city_name):
        current_weather = WeatherAPI.fetch_current_weather(city_name)

        lat = current_weather['coord']['lat']
        lon = current_weather['coord']['lon']

        daily_forecast = WeatherAPI.fetch_5days_forecast(lat, lon)

        city_weather = CityWeather(current_weather)
        city_weather.add_daily_forecast(daily_forecast)

        return city_weather
