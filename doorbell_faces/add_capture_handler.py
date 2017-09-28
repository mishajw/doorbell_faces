from doorbell_faces import face_recognizer
from doorbell_faces import database
import numpy as np


def add_capture(request, _database: database.Database):
    time = request.args.get("time", type=int)
    image = __get_image(request)
    face_embeddings = face_recognizer.recognize_face(image)
    __add_faces_to_database(time, face_embeddings, _database)


def __get_image(request) -> np.array:
    image_columns = request.args.get("image_columns", type=int, default=1920)
    image_rows = request.args.get("image_rows", type=int, default=1080)

    if "file" not in request.files:
        raise ValueError("Couldn't find \"file\" in %s" % list(request.files.keys()))

    file = request.files["file"]

    if file.filename == "":
        raise ValueError("Uploaded file has no name")

    return __load_file_from_stream(file.stream, image_columns, image_rows)


def __load_file_from_stream(stream, image_columns, image_rows) -> np.array:
    file_bytes = stream.read()

    expected_data_size = image_columns * image_rows * 3
    if len(file_bytes) != expected_data_size:
        raise ValueError(
            "Uploaded file is incorrect size, should be 1080p RGB raw data (%d bytes) and got %d bytes"
            % (expected_data_size, len(file_bytes)))

    array = np.frombuffer(file_bytes, dtype=np.uint8)
    array = np.resize(array, [image_columns, image_rows, 3])

    return array


def __add_faces_to_database(time, face_vectors, _database):
    raise NotImplementedError()
