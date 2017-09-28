from doorbell_faces import add_capture_handler
from doorbell_faces import database
from doorbell_faces import exceptions
from doorbell_faces import list_recognitions_handler
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


@app.route("/list_recognitions", methods=["GET"])
def list_recognitions():
    log.info("list_recognitions called")

    # TODO Check if generic .to_json handler in Flask
    return jsonify([result.to_json() for result in list_recognitions_handler.list_recognitions(request, _database)])


@app.errorhandler(exceptions.ServerException)
def server_exception_handler(server_exception: exceptions.ServerException):
    log.warning("Returning exception to user: %s" % server_exception)
    return jsonify(server_exception.to_json()), server_exception.status_code
