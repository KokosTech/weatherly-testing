from datetime import datetime

from flask import Blueprint, render_template, request
from weather_app.models import CityWeather, city_exists

main = Blueprint('main', __name__)
date = datetime.now().strftime("%A %d %B")


@main.route('/')
def index():
    city_name = request.args.get('city') or 'Sofia'
    if not city_exists(city_name):
        return render_template("404.html", error=True, date=date) 
    city_weather = CityWeather.get_weather(city_name)
    return render_template("index.html", city_weather=city_weather, date=date)
