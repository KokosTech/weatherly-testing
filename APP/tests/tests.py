import pytest
import click.testing
from unittest.mock import patch
from weather_app.models import CityWeather, WeatherAPI
from weather_app.exceptions import CityDoesNotExistException
from weather_app import create_app

# Mock response for WeatherAPI
MOCK_VALID_CURRENT_WEATHER_RESPONSE = {
    'name': 'TestCity',
    'sys': {'country': 'TestCountry', 'sunrise': 1633759200, 'sunset': 1633802400},
    'weather': [{'icon': '01d', 'description': 'clear sky'}],
    'main': {'temp': 20.0, 'temp_max': 25.0, 'temp_min': 15.0, 'humidity': 50},
    'wind': {'speed': 10.0},
    'coord': {'lat': 0.0, 'lon': 0.0},
    'cod': 200
}

MOCK_INVALID_CURRENT_WEATHER_RESPONSE = {
    'cod': '404',
    'message': 'city not found'
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


def test_fetch_current_weather_with_invalid_data_that_should_throw_CityDoesNotExistException(mock_requests_get):
    mock_requests_get.return_value.json.return_value = MOCK_INVALID_CURRENT_WEATHER_RESPONSE
    with pytest.raises(CityDoesNotExistException):
        WeatherAPI.fetch_current_weather("TestCity")


def test_fetch_5days_forecast_with_valid_data(mock_requests_get):
    mock_requests_get.return_value.json.return_value = MOCK_VALID_DAILY_FORECAST_RESPONSE
    result = WeatherAPI.fetch_5days_forecast(0.0, 0.0)
    assert result == MOCK_VALID_DAILY_FORECAST_RESPONSE


def test_add_daily_forecast_with_valid_data():
    city_weather = CityWeather(MOCK_VALID_CURRENT_WEATHER_RESPONSE)
    city_weather.add_daily_forecast(MOCK_VALID_DAILY_FORECAST_RESPONSE)
    assert len(city_weather.forecast) == 1


def test_add_daily_forecast_with_None_json_that_should_throw_AssertionError():
    with pytest.raises(AssertionError):
        city_weather = CityWeather(MOCK_VALID_CURRENT_WEATHER_RESPONSE)
        city_weather.add_daily_forecast(None)


def test_add_daily_forecast_with_empty_json_that_should_throw_AssertionError():
    with pytest.raises(AssertionError):
        city_weather = CityWeather(MOCK_VALID_CURRENT_WEATHER_RESPONSE)
        city_weather.add_daily_forecast({})


def test_add_daily_forecast_with_invalid_json_that_should_throw_AssertionError():
    with pytest.raises(AssertionError):
        city_weather = CityWeather(MOCK_VALID_CURRENT_WEATHER_RESPONSE)
        city_weather.add_daily_forecast({'test': 'test'})


def test_get_weather_with_valid_city_name(mock_requests_get):
    mock_requests_get.return_value.json.side_effect = [
        MOCK_VALID_CURRENT_WEATHER_RESPONSE,
        MOCK_VALID_DAILY_FORECAST_RESPONSE
    ]

    result = CityWeather.get_weather("TestCity")

    assert result.name == "TestCity"
    assert result.country == "TestCountry"
    assert result.icon == "01d"
    assert result.description == "Clear Sky"
    assert result.temp == 20
    assert result.high == 25
    assert result.low == 15
    assert result.humidity == 50
    assert result.wind_speed == 10
    assert result.sunrise == "06:00"
    assert result.sunset == "18:00"
    assert len(result.forecast) == 1


def test_get_weather_with_None_that_should_throw_AssetionError(mock_requests_get):
    with pytest.raises(AssertionError):
        CityWeather.get_weather(None)


def test_get_weather_with_empty_string_that_should_throw_AssetionError(mock_requests_get):
    with pytest.raises(AssertionError):
        CityWeather.get_weather("")
