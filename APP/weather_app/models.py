from datetime import datetime
from weather_app.api import WeatherAPI
from weather_app.constants import *
from weather_app.exceptions import InvalidJSONValueException


class CityWeather:
    def _validate_temperature(self, temp):
        if not MIN_TEMP <= temp <= MAX_TEMP:
            raise InvalidJSONValueException(
                f'Temperature must be between {MIN_TEMP} and {MAX_TEMP}')

    def _validate_lat(self, lat):
        if not MIN_LAT <= lat <= MAX_LAT:
            raise InvalidJSONValueException(
                f'Latitude must be between {MIN_LAT} and {MAX_LAT}')

    def _validate_lon(self, lon):
        if not MIN_LON <= lon <= MAX_LON:
            raise InvalidJSONValueException(
                f'Longitude must be between {MIN_LON} and {MAX_LON}')

    def __init__(self, json):
        self.name = json['name']
        self.country = json['sys']['country']
        self.icon = json['weather'][0]['icon']
        self.description = json['weather'][0]['description'].title()

        self.temp = round(json['main']['temp'])
        self._validate_temperature(self.temp)

        self.high = round(json['main']['temp_max'])
        self._validate_temperature(self.high)

        self.low = round(json['main']['temp_min'])
        self._validate_temperature(self.low)

        self.humidity = json['main']['humidity']
        self.wind_speed = round(json['wind']['speed'])
        self.sunrise = datetime.utcfromtimestamp(
            json['sys']['sunrise']).strftime('%H:%M')
        self.sunset = datetime.utcfromtimestamp(
            json['sys']['sunset']).strftime('%H:%M')

        self.lat = json['coord']['lat']
        self._validate_lat(self.lat)

        self.lon = json['coord']['lon']
        self._validate_lon(self.lon)

        self.forecast = []

    def add_daily_forecast(self, json):
        for i in range(0, len(json['daily'])):
            daily = json['daily'][i]

            day = datetime.utcfromtimestamp(daily['dt']).strftime('%a')
            date = datetime.utcfromtimestamp(daily['dt']).strftime('%d/%m')
            icon = daily['weather'][0]['icon']

            low = round(daily['temp']['min'])
            self._validate_temperature(low)
            
            high = round(daily['temp']['max'])
            self._validate_temperature(high)

            wind_speed = round(daily['wind_speed'])
            humidity = daily['humidity']

            self.forecast.append({
                'day': day,
                'date': date,
                'icon': icon,
                'low': low,
                'high': high,
                'wind_speed': wind_speed,
                'humidity': humidity
            })

    @staticmethod
    def get_weather(city_name):
        # We are sure that city_name is not None, not empty and not only whitespace, because we have already validated it in routes.py
        assert city_name is not None, 'City name cannot be None'
        assert city_name != '', 'City name cannot be empty'
        assert not city_name.isspace(), 'City name cannot be only whitespace'

        current_weather = WeatherAPI.fetch_current_weather(city_name)
        city_weather = CityWeather(current_weather)

        daily_forecast = WeatherAPI.fetch_5days_forecast(city_weather.lat, city_weather.lon)
        city_weather.add_daily_forecast(daily_forecast)

        return city_weather
