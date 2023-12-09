from datetime import datetime
from flask import Blueprint, render_template, request
from jsonschema import ValidationError
from weather_app.models import CityWeather
from weather_app.exceptions import CityDoesNotExistException, InvalidCityNameException, InvalidJSONValueException
import cProfile, pstats, io
from pstats import SortKey


main = Blueprint('main', __name__)
date = datetime.now().strftime('%A %d %B')


@main.route('/')
def index():
    city_name = request.args.get('city') or 'Sofia'

    if city_name is None or city_name == '' or city_name.isspace():
        raise InvalidCityNameException

    try:
        pr = cProfile.Profile()
        pr.enable()

        city_weather = CityWeather.get_weather(city_name)

        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        
        return render_template('index.html', city_weather=city_weather, date=date)
    except CityDoesNotExistException:
        return render_template('404.html', error=True, date=date)
    except (InvalidJSONValueException, ValidationError) as exception:
        return render_template('invalid_vendor_data.html', error=True, msg=exception)
