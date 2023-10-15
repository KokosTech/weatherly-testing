from datetime import datetime
from flask import Blueprint, render_template, request
from weather_app.models import CityWeather
from weather_app.exceptions import CityDoesNotExistException

main = Blueprint('main', __name__)
date = datetime.now().strftime("%A %d %B")


@main.route('/')
def index():
    city_name = request.args.get('city') or 'Sofia'

    try:
        city_weather = CityWeather.get_weather(city_name)
        return render_template("index.html", city_weather=city_weather, date=date)
    except CityDoesNotExistException:
        return render_template("404.html", error=True, date=date)
