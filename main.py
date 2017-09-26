import cv2
import os


FACE_CASCADE_FILE = "haarcascade_frontalface_default.xml"
DATA_DIRECTORY = "data"
INPUT_IMAGE_NAME = "input.jpg"
OUTPUT_IMAGE_NAME = "output.jpg"


def main():
    # Set up face detection
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_FILE)

    # Open image
    image = cv2.imread(os.path.join(DATA_DIRECTORY, INPUT_IMAGE_NAME))

    # Detect faces in image
    faces = face_cascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    # Draw detected faces onto image
    for x, y, width, height in faces:
        cv2.rectangle(image, (x, y), ((x + width), (y + height)), (0, 255, 0), 2)

    # Write out image
    if not os.path.isdir(DATA_DIRECTORY):
        os.mkdir(DATA_DIRECTORY)
    cv2.imwrite(os.path.join(DATA_DIRECTORY, OUTPUT_IMAGE_NAME), image)


if __name__ == "__main__":
    main()
