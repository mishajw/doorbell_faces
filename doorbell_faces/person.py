from doorbell_faces import database
from doorbell_faces import recognition
from typing import Optional, List
from flask_restful import Resource
from flask_restful import reqparse


class Person:
    def __init__(self, name: Optional[str], recognitions: List["recognition.Recognition"]):
        self.name = name
        self.recognitions = recognitions

    def to_json(self) -> dict:
        return {
            "name": self.name
        }

    @staticmethod
    def get_resource(_database: database.Database):
        put_parser = reqparse.RequestParser()
        put_parser.add_argument("name", type=str, required=False)

        class PersonResource(Resource):
            def get(self):
                cursor = _database.execute("""SELECT name FROM person""")
                name = cursor.fetchone()
                assert len(name) > 0

                return Person(name, []).to_json()

            def put(self):
                args = put_parser.parse_args()
                _database.execute("""INSERT INTO person (name) VALUES (?)""", (args.name,))
                _database.commit()

        return PersonResource
