from datetime import datetime
from flask import Blueprint, render_template, request
from jsonschema import ValidationError
from weather_app.models import CityWeather
from weather_app.exceptions import *

main = Blueprint('main', __name__)
date = datetime.now().strftime('%A %d %B')


@main.route('/')
def index():
    city_name = request.args.get('city') or 'Sofia'

    if city_name is None or city_name == '' or city_name.isspace():
        raise InvalidCityNameException

    try:
        city_weather = CityWeather.get_weather(city_name)
        return render_template('index.html', city_weather=city_weather, date=date)
    except CityDoesNotExistException:
        return render_template('404.html', error=True, date=date)
    except InvalidJSONValueException or ValidationError as exception:
        return render_template('invalid_vendor_data.html', error=True, msg=exception)
