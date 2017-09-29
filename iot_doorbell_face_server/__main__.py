from iot_doorbell_face_server import server
import configargparse
import logging
import sys


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    parser = configargparse.ArgParser("iot-doorbell-face-server")
    parser.add_argument(
        "-c",
        "--config",
        default="iot-doorbell-face-server.ini",
        help="Configuration file for server",
        is_config_file=True,
        env_var="CONFIG")
    parser.add_argument("-p", "--port", required=True, help="Port for the server to listen on", env_var="PORT")
    parser.add_argument(
        "-s", "--capture_path", help="Where to store capture files", default="data/captures", env_var="CAPTURE_PATH")
    parser.add_argument(
        "-d",
        "--database_file_path",
        help="Where to database file",
        default="data/database.db",
        env_var="DATABASE_FILE_PATH")

    args = parser.parse_args()
    server.run(port=args.port, database_file_path=args.database_file_path, capture_path=args.capture_path)
