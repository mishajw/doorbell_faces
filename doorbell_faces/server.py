from doorbell_faces import database
from doorbell_faces import person
from flask import Flask
from flask_restful import Api
import sqlite3


def run():
    _database = database.get_database()

    flask_app = Flask("doorbell_faces")
    flask_api = Api(flask_app)
    flask_api.add_resource(person.Person.get_resource(_database), "/person")

    flask_app.run(port=12612)
