import pytest
from unittest.mock import patch
from APP.weather_app.models import CityWeather, WeatherAPI

# Mock response for WeatherAPI
MOCK_VALID_CURRENT_WEATHER_RESPONSE = {
    'name': 'TestCity',
    'sys': {'country': 'TestCountry', 'sunrise': 1633759200, 'sunset': 1633802400},
    'weather': [{'icon': '01d', 'description': 'clear sky'}],
    'main': {'temp': 20.0, 'temp_max': 25.0, 'temp_min': 15.0, 'humidity': 50},
    'wind': {'speed': 10.0},
    'coord': {'lat': 0.0, 'lon': 0.0}
}

MOCK_VALID_DAILY_FORECAST_RESPONSE = {
    'daily': [
        {
            'dt': 1633852800,
            'weather': [{'icon': '01d'}],
            'temp': {'min': 15.0, 'max': 25.0},
            'wind_speed': 12.0,
            'humidity': 45
        },
        # ... more forecast data for the next days ...
    ]
}

@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get

def test_fetch_current_weather_with_valid_data(mock_requests_get):
    mock_requests_get.return_value.json.return_value = MOCK_VALID_CURRENT_WEATHER_RESPONSE
    result = WeatherAPI.fetch_current_weather("TestCity")
    assert result == MOCK_VALID_CURRENT_WEATHER_RESPONSE

def test_add_daily_forecast_with_valid_data():
    city_weather = CityWeather(MOCK_VALID_CURRENT_WEATHER_RESPONSE)
    city_weather.add_daily_forecast(MOCK_VALID_DAILY_FORECAST_RESPONSE)
    assert len(city_weather.forecast) == 1

def test_add_daily_forecast_with_invalid_data_that_should_throw_AssertionError():
    with pytest.raises(AssertionError):
        CityWeather.get_weather("")
