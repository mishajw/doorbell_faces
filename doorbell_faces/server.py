from doorbell_faces import add_capture_handler
from doorbell_faces import database
from flask import Flask, request

app = Flask("doorbell_faces")
_database = database.get_database()


def run():
    app.run(port=12612)


@app.route("/add_capture", methods=["POST"])
def add_capture():
    try:
        return add_capture_handler.add_capture(request, _database)
    except ValueError as e:
        return wrap_exception(e)


def wrap_exception(exception: Exception):
    return str({
        "error": str(exception)
    })
