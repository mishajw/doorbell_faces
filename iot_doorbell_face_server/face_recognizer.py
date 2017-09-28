from typing import List
import face_recognition
import numpy as np


def recognize_face(image: np.array) -> List[np.array]:
    face_locations = face_recognition.face_locations(image)
    face_embeddings = face_recognition.face_encodings(image, face_locations)

    return face_embeddings
