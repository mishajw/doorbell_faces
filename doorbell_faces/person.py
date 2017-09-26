from doorbell_faces import recognition
from typing import Optional, List
from flask_restful import Resource


class Person:
    def __init__(self, name: Optional[str], recognitions: List["recognition.Recognition"]):
        self.name = name
        self.recognitions = recognitions

    def to_json(self) -> dict:
        return {
            "name": self.name
        }


class PersonResource(Resource):
    def __init__(self):
        self.__name__ = "PersonResource"

    def get(self):
        return Person("John Smith", []).to_json()
