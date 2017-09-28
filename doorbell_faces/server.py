from doorbell_faces import add_capture_handler
from doorbell_faces import database
from doorbell_faces import exceptions
from flask import Flask, request, jsonify
import logging

log = logging.getLogger(__name__)

app = Flask("doorbell_faces")
_database = database.get_database()


def run():
    log.info("Starting server")
    app.run(port=12612)


@app.route("/add_capture", methods=["POST"])
def add_capture():
    log.info("add_capture called")

    # TODO Return standardised values
    try:
        add_capture_handler.add_capture(request, _database)
        return "success"
    except exceptions.ServerException as server_exception:
        return jsonify(server_exception.to_json()), server_exception.status_code
