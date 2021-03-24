"""An example of a single page Flask application"""

from datetime import datetime
from os import getenv
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
DB = SQLAlchemy(app)


# app routes
# @ is a python decorater notation


@app.route("/")
def hello_world():
    # Querying from our new database
    astro_data = Astronauts.query.all()[0]
    return "There are {} astronauts in space at {}!".format(
        astro_data.num_astros, astro_data.time_stamp
    )


@app.route("/refresh")
def refresh():
    request = requests.get("http://api.open-notify.org/astros.json")
    astro_data = request.json()
    api_astro_info = astro_data["number"]
    record = Astronauts(
        num_astros=api_astro_info, time_stamp=str(datetime.now())
    )
    DB.session.add(record)
    DB.session.commit()
    return "Database updated!"


@app.route("/reset")
def reset():
    DB.drop_all()
    DB.create_all()
    return "Database reset!"


# Create Astronauts table using SQLAlchemy
class Astronauts(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    num_astros = DB.Column(DB.Integer, nullable=False)
    time_stamp = DB.Column(DB.String(30))

    def __repr__(self):
        return "# of astronauts: {}".format(self.num_astros)
