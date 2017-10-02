from iot_doorbell_face_server import add_capture_handler
from iot_doorbell_face_server import get_capture_handler
from iot_doorbell_face_server import database
from iot_doorbell_face_server import exceptions
from iot_doorbell_face_server import list_recognitions_handler
from flask import Flask, request, jsonify, send_file
from flask.views import View
import logging
import time

log = logging.getLogger(__name__)


def run(port: int, database_file_path: str, capture_path):
    log.info("Connecting to database")
    _database = database.get_database(database_file_path)

    log.info("Starting server")
    app = Flask("iot-doorbell-face-server")
    app.add_url_rule(
        "/add_capture", view_func=AddCaptureView.as_view("add_capture", capture_path, _database), methods=["POST"])
    app.add_url_rule(
        "/list_recognitions", view_func=ListRecognitionsView.as_view("list_recognitions", _database))
    app.add_url_rule("/get_capture", view_func=GetCaptureView.as_view("get_capture", _database))
    app.errorhandler(exceptions.ServerException)(server_exception_handler)
    app.run(host="0.0.0.0", port=port)


class AddCaptureView(View):
    methods = ["POST"]

    def __init__(self, capture_directory: str, _database: database.Database):
        self.capture_directory = capture_directory
        self.database = _database

    def dispatch_request(self):
        log.info("add_capture called")

        _time = request.args.get("time", type=int)
        image_width = request.args.get("image_columns", type=int, default=1920)
        image_height = request.args.get("image_rows", type=int, default=1080)
        image_stream = get_file_stream()

        add_capture_handler.add_capture(
            _time, image_width, image_height, image_stream, self.capture_directory, self.database)

        # TODO Return correct value
        return "success"


class ListRecognitionsView(View):
    methods = ["GET"]

    def __init__(self, _database: database.Database):
        self.database = _database

    def dispatch_request(self):
        log.info("list_recognitions called")

        start_time = request.args.get("start_time", type=int, default=0)
        end_time = request.args.get("end_time", type=int, default=get_current_unix_time())

        results = list_recognitions_handler.list_recognitions(start_time, end_time, self.database)

        # TODO Check if generic .to_json handler in Flask
        return jsonify([result.to_json() for result in results])


class GetCaptureView(View):
    methods = ["GET"]

    def __init__(self, capture_directory: str, _database: database.Database):
        self.capture_directory = capture_directory
        self.database = _database

    def dispatch_request(self):
        log.info("get_capture called")

        capture_hash = request.args.get("capture_hash", type=str, default=None)
        capture_id = request.args.get("capture_id", type=int, default=None)

        if capture_hash is not None:
            capture_image_path = get_capture_handler.get_capture_from_hash(
                capture_hash, self.capture_directory, self.database)
        elif capture_id is not None:
            capture_image_path = get_capture_handler.get_capture_from_id(
                capture_id, self.capture_directory, self.database)
        else:
            raise exceptions.IncorrectValueException.from_message(
                "One of \"capture_hash\" or \"capture_id\" must be set")

        return send_file(capture_image_path)


def server_exception_handler(server_exception: exceptions.ServerException):
    log.warning("Returning exception to user: %s" % server_exception)
    return jsonify(server_exception.to_json()), server_exception.status_code


def get_file_stream():
    if "file" not in request.files:
        raise exceptions.IncorrectValueException.from_value_and_explanation(
            "files", list(request.files), "doesn't contain  \"file\"")

    file = request.files["file"]

    if file.filename == "":
        raise exceptions.IncorrectValueException.from_value_and_explanation("file.filename", file.filename, "is empty")

    return file.stream


def get_current_unix_time() -> int:
    return int(time.time() * 1000)
