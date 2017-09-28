from iot_doorbell_face_server import add_capture_handler
from iot_doorbell_face_server import get_capture_handler
from iot_doorbell_face_server import database
from iot_doorbell_face_server import exceptions
from iot_doorbell_face_server import list_recognitions_handler
from flask import Flask, request, jsonify, send_file
import logging
import time

log = logging.getLogger(__name__)

app = Flask("iot-doorbell-face-server")
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


@app.route("/get_capture", methods=["GET"])
def get_capture():
    log.info("get_capture called")

    capture_hash = request.args.get("capture_hash", type=str, default=None)
    capture_id = request.args.get("capture_id", type=int, default=None)

    if capture_hash is not None:
        capture_image_path = get_capture_handler.get_capture_from_hash(capture_hash, _database)
    elif capture_id is not None:
        capture_image_path = get_capture_handler.get_capture_from_id(capture_id, _database)
    else:
        raise exceptions.IncorrectValueException.from_message("One of \"capture_hash\" or \"capture_id\" must be set")

    return send_file(capture_image_path)


@app.errorhandler(exceptions.ServerException)
def server_exception_handler(server_exception: exceptions.ServerException):
    log.warning("Returning exception to user: %s" % server_exception)
    return jsonify(server_exception.to_json()), server_exception.status_code


@app.errorhandler(NotImplementedError)
def not_implemented_error_handler(_: NotImplementedError):
    return "Functionality not implemented", 500


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
