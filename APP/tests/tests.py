import pytest
from copy import deepcopy
from unittest.mock import patch, Mock
from jsonschema import ValidationError
from app import app
from weather_app.models import CityWeather, WeatherAPI
from weather_app.exceptions import *
from tests.mock_data import *


@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get


# WeatherAPI tests
def test_fetch_current_weather_with_valid_data(mock_requests_get, benchmark):
    mock_requests_get.return_value.json.return_value = MOCK_VALID_CURRENT_WEATHER_RESPONSE
    result = benchmark(WeatherAPI.fetch_current_weather, 'TestCity')
    assert result == MOCK_VALID_CURRENT_WEATHER_RESPONSE


def test_fetch_current_weather_with_invalid_json_response_that_should_throw_ValidationError(mock_requests_get):
    mock_requests_get.return_value.json.return_value = MOCK_INVALID_CURRENT_WEATHER_RESPONSE
    with pytest.raises(ValidationError):
        WeatherAPI.fetch_current_weather('TestCity')


def test_fetch_current_weather_with_invalid_city_name_that_should_throw_CityDoesNotExistException(mock_requests_get):
    mock_requests_get.return_value.json.return_value = MOCK_CITY_NOT_FOUND_RESPONSE
    with pytest.raises(CityDoesNotExistException):
        WeatherAPI.fetch_current_weather('TestCity')


def test_fetch_5days_forecast_with_valid_data(mock_requests_get, benchmark):
    mock_requests_get.return_value.json.return_value = MOCK_VALID_DAILY_FORECAST_RESPONSE
    result = benchmark(WeatherAPI.fetch_5days_forecast, 0.0, 0.0)
    assert result == MOCK_VALID_DAILY_FORECAST_RESPONSE


def test_fetch_5days_forecast_with_invalid_json_response_that_should_throw_ValidationError(mock_requests_get):
    mock_requests_get.return_value.json.return_value = MOCK_INVALID_DAILY_FORECAST_RESPONSE
    with pytest.raises(ValidationError):
        WeatherAPI.fetch_5days_forecast(0.0, 0.0)


# CityWeather tests
def test_add_daily_forecast_with_valid_data():
    city_weather = CityWeather(MOCK_VALID_CURRENT_WEATHER_RESPONSE)
    city_weather.add_daily_forecast(MOCK_VALID_DAILY_FORECAST_RESPONSE)
    assert len(city_weather.forecast) == 1


def test_add_daily_forecast_with_invalid_min_temp_that_should_throw_InvalidJSONValueException():
    with pytest.raises(InvalidJSONValueException):
        city_weather = CityWeather(MOCK_VALID_CURRENT_WEATHER_RESPONSE)

        invalid_json = deepcopy(MOCK_VALID_DAILY_FORECAST_RESPONSE)
        invalid_json['daily'][0]['temp']['min'] = -120

        city_weather.add_daily_forecast(invalid_json)


def test_add_daily_forecast_with_invalid_max_temp_that_should_throw_InvalidJSONValueException():
    with pytest.raises(InvalidJSONValueException):
        city_weather = CityWeather(MOCK_VALID_CURRENT_WEATHER_RESPONSE)

        invalid_json = deepcopy(MOCK_VALID_DAILY_FORECAST_RESPONSE)
        invalid_json['daily'][0]['temp']['max'] = 120

        city_weather.add_daily_forecast(invalid_json)


def test_get_weather_with_valid_data(mock_requests_get):
    mock_requests_get.return_value.json.side_effect = [
        MOCK_VALID_CURRENT_WEATHER_RESPONSE,
        MOCK_VALID_DAILY_FORECAST_RESPONSE
    ]

    result = CityWeather.get_weather('TestCity')

    assert result.name == 'TestCity'
    assert result.country == 'TestCountry'
    assert result.icon == '01d'
    assert result.description == 'Clear Sky'
    assert result.temp == 20
    assert result.high == 25
    assert result.low == 15
    assert result.humidity == 50
    assert result.wind_speed == 10
    assert result.sunrise == '06:00'
    assert result.sunset == '18:00'
    assert len(result.forecast) == 1


def test_get_weather_with_invalid_min_temp_that_should_throw_InvalidJSONValueException(mock_requests_get):
    invalid_json = deepcopy(MOCK_VALID_CURRENT_WEATHER_RESPONSE)
    invalid_json['main']['temp_min'] = -120

    mock_requests_get.return_value.json.side_effect = [
        invalid_json,
        MOCK_VALID_DAILY_FORECAST_RESPONSE
    ]

    with pytest.raises(InvalidJSONValueException):
        CityWeather.get_weather('TestCity')


def test_get_weather_with_invalid_max_temp_that_should_throw_InvalidJSONValueException(mock_requests_get):
    invalid_json = deepcopy(MOCK_VALID_CURRENT_WEATHER_RESPONSE)
    invalid_json['main']['temp_max'] = 120

    mock_requests_get.return_value.json.side_effect = [
        invalid_json,
        MOCK_VALID_DAILY_FORECAST_RESPONSE
    ]

    with pytest.raises(InvalidJSONValueException):
        CityWeather.get_weather('TestCity')


def test_get_weather_with_invalid_lat_that_should_throw_InvalidJSONValueException(mock_requests_get):
    invalid_json = deepcopy(MOCK_VALID_CURRENT_WEATHER_RESPONSE)
    invalid_json['coord']['lat'] = -500

    mock_requests_get.return_value.json.side_effect = [
        invalid_json,
        MOCK_VALID_DAILY_FORECAST_RESPONSE
    ]

    with pytest.raises(InvalidJSONValueException):
        CityWeather.get_weather('TestCity')


def test_get_weather_with_invalid_lon_that_should_throw_InvalidJSONValueException(mock_requests_get):
    invalid_json = deepcopy(MOCK_VALID_CURRENT_WEATHER_RESPONSE)
    invalid_json['coord']['lon'] = 500

    mock_requests_get.return_value.json.side_effect = [
        invalid_json,
        MOCK_VALID_DAILY_FORECAST_RESPONSE
    ]

    with pytest.raises(InvalidJSONValueException):
        CityWeather.get_weather('TestCity')


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Routes tests
def test_index_route_with_valid_city(client, benchmark):
    with patch('weather_app.models.CityWeather.get_weather') as mock_get_weather:
        mock_city_weather = Mock(spec=CityWeather)
        mock_city_weather.name = 'Sofia'
        mock_get_weather.return_value = mock_city_weather

        response = benchmark(client.get, '/?city=Sofia')

        mock_get_weather.assert_called_with('Sofia')
        assert b'Sofia' in response.data


def test_index_route_with_non_existing_city(client):
    with patch('weather_app.models.CityWeather.get_weather') as mock_get_weather:
        mock_get_weather.side_effect = CityDoesNotExistException

        response = client.get('/?city=NonExistentCity')

        mock_get_weather.assert_called_with('NonExistentCity')
        assert b'Page not found' in response.data
