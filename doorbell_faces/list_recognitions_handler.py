from doorbell_faces import database
from doorbell_faces import exceptions
import time


class ListRecognitionsResult:
    def __init__(self, person_id: int, person_name: str, capture_id: int, capture_time: int, capture_hash: str):
        self.person_id = person_id
        self.person_name = person_name
        self.capture_id = capture_id
        self.capture_time = capture_time
        self.capture_hash = capture_hash

    def to_json(self) -> str:
        return str({
            "person": {
                "person_id": self.person_id,
                "person_name": self.person_name
            },
            "capture": {
                "capture_id": self.capture_id,
                "capture_time": self.capture_time,
                "capture_hash": self.capture_hash
            }
        })


def list_recognitions(request, _database: database.Database):
    # TODO: Paginate

    start_time = request.args.get("start_time", type=int, default=0)
    end_time = request.args.get("end_time", type=int, default=__get_current_unix_time())

    if end_time < start_time:
        raise exceptions.IncorrectValueException.from_value_and_explanation(
            "(start_time, end_time)", (start_time, end_time), "start time must be before end time")

    cursor = _database.cursor()

    cursor.execute(
        """
          SELECT person.person_id, person.name, capture.capture_id, capture.time, capture.hash
          FROM person, capture, recognition
          WHERE 
            person.person_id = recognition.person_id AND
            recognition.capture_id = capture.capture_id AND
            capture.time > ? AND
            capture.time < ?
        """,
        (start_time, end_time))

    return [ListRecognitionsResult(*result) for result in cursor.fetchall()]


def __get_current_unix_time() -> int:
    return int(time.time() * 1000)
