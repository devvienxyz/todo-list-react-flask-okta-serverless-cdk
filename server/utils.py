import uuid
import cv2
import os
import sys
import logging
from datetime import datetime
from settings.config import IS_PROD


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
logger.setLevel(logging.INFO if IS_PROD else logging.DEBUG)


def error_if_exists(filename):
    if bool(os.path.exists(filename)):
        raise ValueError(f"{filename} already exists.")


def error_if_not_empty(output_dir):
    if bool(os.listdir(output_dir)):
        raise ValueError(f"{output_dir} is not empty.")


def get_video_or_raise_error(video_path):
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise FileNotFoundError(f"Unable to open video file: {video_path}")

    return video


# ANSI escape code
GREEN = "\033[92m"
BLUE = "\033[34m"
RESET = "\033[0m"


def success_message(message):
    sys.stdout.write(GREEN + message + RESET + "\n")


def info_message(message):
    sys.stdout.write(BLUE + message + RESET + "\n")


def get_time_now_in_str_epoch() -> str:
    return str(int(datetime.now().timestamp()))


def generate_uuid() -> str:
    return str(uuid.uuid4())
