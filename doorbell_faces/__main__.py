from doorbell_faces import server
import logging
import sys


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    server.run(port=12612)
