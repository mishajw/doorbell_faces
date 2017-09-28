import doorbell_faces
import logging
import sys


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    doorbell_faces.server.run(port=12612)


if __name__ == "__main__":
    main()
