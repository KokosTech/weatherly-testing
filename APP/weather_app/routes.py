from flask import render_template, Blueprint
from datetime import datetime
from weather_app.models import CityWeather


main = Blueprint('main', __name__)
date = datetime.now().strftime("%A %d %B")


@main.route('/')
def index():
    city_name = 'Sofia'
    city_weather = CityWeather.get_weather(city_name)
    return render_template("index.html", city_weather=city_weather, date=date)


@main.route('/<city_name>')
def weather(city_name):
    city_weather = CityWeather.get_weather(city_name)
    return render_template("index.html", city_weather=city_weather, date=date)
