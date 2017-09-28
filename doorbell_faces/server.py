from doorbell_faces import add_capture_handler
from doorbell_faces import database
from doorbell_faces import exceptions
from flask import Flask, request, jsonify
import logging

log = logging.getLogger(__name__)

app = Flask("doorbell_faces")
_database = database.get_database()


def run(port: int):
    log.info("Starting server")
    app.run(port=port)


@app.route("/add_capture", methods=["POST"])
def add_capture():
    log.info("add_capture called")

    add_capture_handler.add_capture(request, _database)

    # TODO Return correct value
    return "success"


@app.errorhandler(exceptions.ServerException)
def server_exception_handler(server_exception: exceptions.ServerException):
    log.warning("Returning exception to user: %s" % server_exception)
    return jsonify(server_exception.to_json()), server_exception.status_code
