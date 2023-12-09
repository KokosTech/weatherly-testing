from flask import Flask
from dotenv import load_dotenv
from weather_app.routes import main
import flask_profiler


def create_app():
    app = Flask(__name__)

    app.config["DEBUG"] = True

    app.config["flask_profiler"] = {
        "enabled": app.config["DEBUG"],
        "storage": {
            "engine": "sqlite"
        },
        "basicAuth":{
            "enabled": True,
            "username": "admin",
            "password": "admin"
        },
        "ignore": [
            "^/static/.*"
        ]
    }

    load_dotenv()
    app.register_blueprint(main)

    flask_profiler.init_app(app)
    
    return app
