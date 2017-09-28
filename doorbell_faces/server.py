from doorbell_faces import add_capture_handler
from doorbell_faces import database
from doorbell_faces import exceptions
from doorbell_faces import list_recognitions_handler
from flask import Flask, request, jsonify
import logging
import time

log = logging.getLogger(__name__)

app = Flask("doorbell_faces")
_database = database.get_database()


def run(port: int):
    log.info("Starting server")
    app.run(port=port)


@app.route("/add_capture", methods=["POST"])
def add_capture():
    log.info("add_capture called")

    time = request.args.get("time", type=int)
    image_width = request.args.get("image_columns", type=int, default=1920)
    image_height = request.args.get("image_rows", type=int, default=1080)
    image_stream = __get_file_stream()

    add_capture_handler.add_capture(time, image_width, image_height, image_stream, _database)

    # TODO Return correct value
    return "success"


@app.route("/list_recognitions", methods=["GET"])
def list_recognitions():
    log.info("list_recognitions called")

    start_time = request.args.get("start_time", type=int, default=0)
    end_time = request.args.get("end_time", type=int, default=__get_current_unix_time())

    results = list_recognitions_handler.list_recognitions(start_time, end_time, _database)

    # TODO Check if generic .to_json handler in Flask
    return jsonify([result.to_json() for result in results])


@app.errorhandler(exceptions.ServerException)
def server_exception_handler(server_exception: exceptions.ServerException):
    log.warning("Returning exception to user: %s" % server_exception)
    return jsonify(server_exception.to_json()), server_exception.status_code


def __get_file_stream():
    if "file" not in request.files:
        raise exceptions.IncorrectValueException.from_value_and_explanation(
            "files", list(request.files), "doesn't contain  \"file\"")

    file = request.files["file"]

    if file.filename == "":
        raise exceptions.IncorrectValueException.from_value_and_explanation("file.filename", file.filename, "is empty")

    return file.stream


def __get_current_unix_time() -> int:
    return int(time.time() * 1000)
