from face_server import recognition
from typing import Optional, List


class Person:
    def __init__(self, name: Optional[str], recognitions: List["recognition.Recognition"]):
        self.name = name
        self.recognitions = recognitions
