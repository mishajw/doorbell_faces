from doorbell_faces import database
from doorbell_faces import exceptions
from doorbell_faces import face_recognizer
from typing import List, Optional
import hashlib
import logging
import numpy as np

log = logging.getLogger(__name__)


def add_capture(request, _database: database.Database):
    time = request.args.get("time", type=int)
    image = __get_image(request)
    log.info("Received image of shape %s and time of %d" % (image.shape, time))

    capture_id = __add_capture_to_database(image, time, _database)
    face_embeddings = face_recognizer.recognize_face(image)
    __add_faces_to_database(face_embeddings, capture_id, _database)
    _database.commit()

    log.info("Added all %d recognitions to database" % len(face_embeddings))


def __get_image(request) -> np.array:
    image_columns = request.args.get("image_columns", type=int, default=1920)
    image_rows = request.args.get("image_rows", type=int, default=1080)

    if "file" not in request.files:
        raise exceptions.IncorrectValueException.from_value_and_explanation(
            "files", list(request.files), "doesn't contain  \"file\"")

    file = request.files["file"]

    if file.filename == "":
        raise exceptions.IncorrectValueException.from_value_and_explanation("file.filename", file.filename, "is empty")

    return __load_file_from_stream(file.stream, image_columns, image_rows)


def __load_file_from_stream(stream, image_columns, image_rows) -> np.array:
    file_bytes = stream.read()

    expected_data_size = image_columns * image_rows * 3
    if len(file_bytes) != expected_data_size:
        raise exceptions.IncorrectValueException.from_message(
            "Uploaded file is incorrect size, should be 1080p RGB raw data (%d bytes) and got %d bytes"
            % (expected_data_size, len(file_bytes)))

    array = np.frombuffer(file_bytes, dtype=np.uint8)
    array = np.resize(array, [image_columns, image_rows, 3])

    return array


def __add_faces_to_database(new_face_embeddings: List[np.array], capture_id: int, _database: database.Database):
    cursor = _database.cursor()

    cursor.execute("""
      SELECT person.person_id, recognition.face_embedding
      FROM
        person, recognition
      WHERE
        person.person_id = recognition.person_id
    """)

    results = [
        (person_id, np.frombuffer(face_embedding_data, dtype=np.float64))
        for person_id, face_embedding_data in cursor.fetchall()]

    def compare_embeddings(face_embedding1: np.array, face_embedding2: np.array):
        return np.average(np.abs(np.subtract(face_embedding1, face_embedding2)))

    for new_face_embedding in new_face_embeddings:
        closest = sorted(
            results, key=(lambda face: compare_embeddings(face[1], new_face_embedding)))

        # If there are other faces in the database...
        if len(closest) > 0:
            # Record the closest face
            closest_person_id, closest_face_embedding = closest[0]

            # Remove the closest face if the embeddings are too far away from each other
            if compare_embeddings(closest_face_embedding, new_face_embedding) > 0.6:
                closest_person_id = None
        else:
            closest_person_id = None

        __add_recognition_to_database(closest_person_id, capture_id, new_face_embedding, _database)


def __add_capture_to_database(image: np.array, time: int, _database: database.Database) -> int:
    cursor = _database.cursor()

    cursor.execute(
        """
          INSERT INTO capture (time, hash) VALUES (?, ?)
        """,
        (time, __hash_numpy_array(image)))

    capture_id = cursor.lastrowid

    log.info("Added capture to database with ID %d" % capture_id)

    return capture_id


def __add_recognition_to_database(
        person_id: Optional[int], capture_id: int, face_embedding: np.array, _database: database.Database) -> int:

    cursor = _database.cursor()

    if person_id is None:
        cursor.execute("""
          INSERT INTO person (name) VALUES (NULL)
        """)
        person_id = cursor.lastrowid
        log.info("Added new person to database with ID %d" % person_id)

    cursor.execute(
        """
          INSERT INTO recognition (person_id, capture_id, face_embedding)
          VALUES (?, ?, ?)
        """,
        (person_id, capture_id, face_embedding.tobytes()))

    recognition_id = cursor.lastrowid

    log.info("Added new recognition to database with ID %d" % recognition_id)

    return recognition_id


def __hash_numpy_array(a: np.array) -> str:
    return hashlib.sha1(a.flatten().view(dtype=np.float64)).hexdigest()
