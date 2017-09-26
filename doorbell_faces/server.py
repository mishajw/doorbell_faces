from flask import Flask
from flask_restful import Api
from doorbell_faces import person


def run():
    flask_app = Flask("doorbell_faces")
    flask_api = Api(flask_app)
    flask_api.add_resource(person.PersonResource(), "/person")

    flask_app.run(port=12612)
