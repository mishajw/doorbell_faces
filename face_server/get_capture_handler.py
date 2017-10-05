from face_server import database
from face_server import exceptions
import os


def get_capture_from_hash(capture_hash: str, capture_directory: str, _database: database.Database) -> str:
    capture_path = os.path.abspath(os.path.join(capture_directory, "%s.npy" % capture_hash))

    if not os.path.isfile(capture_path):
        raise exceptions.IncorrectValueException.from_value_and_explanation(
            "capture_hash", capture_hash, "does not exist")

    return capture_path


def get_capture_from_id(capture_id: int, capture_directory: str, _database: database.Database) -> str:
    raise exceptions.UnimplementedException()  # TODO
