from collections import namedtuple
from typing import List
import cv2
import numpy as np


# Used to detect faces
__FACE_CASCADE_FILE = "haarcascade_frontalface_default.xml"
__face_cascade = None


DetectedFace = namedtuple("DetectedFace", ["x", "y", "width", "height"])


def detect_faces(image: np.array) -> List[DetectedFace]:
    # Create the face cascade if it hasn't been created before
    global __face_cascade
    if __face_cascade is None:
        __face_cascade = cv2.CascadeClassifier(__FACE_CASCADE_FILE)

    # Detect faces in image
    faces = __face_cascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    return [DetectedFace(*face) for face in faces]
