import logging
import os
import sys

from .constants import Env

# Determine log level
log_levels = {
    Env.LOCAL: logging.DEBUG,
    Env.DEV: logging.INFO,
    Env.TEST: logging.WARNING,
    Env.PROD: logging.ERROR,
}
env = Env[os.getenv("ENV").upper()]
log_level = log_levels[env]

# Create logger
logger = logging.getLogger()
formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
# file_handler = logging.FileHandler("app.log")
# file_handler.setFormatter(formatter)
logger.handlers = [
    stream_handler,
]
logger.setLevel(log_level)
