from doorbell_faces import database
from doorbell_faces import exceptions
import os

CAPTURE_DIRECTORY = "data/capture"


def get_capture_from_hash(capture_hash: str, _database: database.Database) -> str:
    capture_path = os.path.abspath(os.path.join(CAPTURE_DIRECTORY, "%s.npy" % capture_hash))

    if not os.path.isfile(capture_path):
        raise exceptions.IncorrectValueException.from_value_and_explanation(
            "capture_hash", capture_hash, "does not exist")

    return capture_path


def get_capture_from_id(capture_id: int, _database: database.Database) -> str:
    raise NotImplementedError()  # TODO
