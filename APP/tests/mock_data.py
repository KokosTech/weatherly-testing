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
    'test': 'test',
    'cod': 200
}

MOCK_CITY_NOT_FOUND_RESPONSE = {
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
    ]
}

MOCK_INVALID_DAILY_FORECAST_RESPONSE = {
    'test': 'test'
}