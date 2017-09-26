from doorbell_faces import person
from doorbell_faces import capture


class Recognition:
    def __init__(
            self,
            _person: "person.Person",
            _capture: "capture.Capture",
            x: float,
            y: float,
            width: float,
            height: float):
        self.person = person
        self.capture = capture
        self.x = x
        self.y = y
        self.width = width
        self.height = height
