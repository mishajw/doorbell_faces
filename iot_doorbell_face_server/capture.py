from iot_doorbell_face_server import recognition
import numpy as np


class Capture:
    def __init__(self, time: int, _recognitions: recognition.Recognition):
        self.time = time
        self.recognitions = _recognitions

    def get_image(self) -> np.array:
        raise NotImplementedError()
