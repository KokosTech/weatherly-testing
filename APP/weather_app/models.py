from datetime import datetime
from weather_app.api import WeatherAPI


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
        self.sunrise = datetime.utcfromtimestamp(
            json['sys']['sunrise']).strftime('%H:%M')
        self.sunset = datetime.utcfromtimestamp(
            json['sys']['sunset']).strftime('%H:%M')
        self.forecast = []

    def add_daily_forecast(self, json):
        assert json is not None, "JSON cannot be None"
        assert json != {}, "JSON cannot be empty"
        assert 'daily' in json, "JSON must contain 'daily' key"

        for i in range(0, len(json['daily'])):
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
        assert city_name is not None, "City name cannot be None"
        assert city_name != "", "City name cannot be empty"

        current_weather = WeatherAPI.fetch_current_weather(city_name)

        lat = current_weather['coord']['lat']
        lon = current_weather['coord']['lon']

        daily_forecast = WeatherAPI.fetch_5days_forecast(lat, lon)

        city_weather = CityWeather(current_weather)
        city_weather.add_daily_forecast(daily_forecast)

        return city_weather
