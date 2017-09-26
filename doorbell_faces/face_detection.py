from collections import namedtuple
from doorbell_faces import capture
from typing import List
import cv2


# Used to detect faces
__FACE_CASCADE_FILE = "haarcascade_frontalface_default.xml"
__face_cascade = None


DetectedFace = namedtuple("DetectedFace", ["x", "y", "width", "height"])


def detect_faces(_capture: capture.Capture) -> List[DetectedFace]:
    # Create the face cascade if it hasn't been created before
    global __face_cascade
    if __face_cascade is None:
        __face_cascade = cv2.CascadeClassifier(__FACE_CASCADE_FILE)

    image = _capture.get_image()

    # Detect faces in image
    faces = __face_cascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    return [DetectedFace(*face) for face in faces]
