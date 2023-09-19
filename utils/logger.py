"""
This class is responsable for defining the logging that will be used throughtout the program.
"""
# pylint: disable=C0413
from pathlib import Path
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from utils.variables import LOG_FILE, LOG_FOLDER, LOG_LEVEL, LOG_RETENTION

now = datetime.now()
date = now.strftime("%Y-%m-%d")

class Logger():
    """Logger Class"""

    def __init__(self, name: str):
        self.name = name

    def verification(self):
        """
        This method is responsible for verifying that the necessary 
        folder and archive are created and with the correct format.
        Return:
            full_path (str): Stores the full path where the logs will be stored.
        """
        log_folder = Path(LOG_FOLDER)
        if not log_folder.exists():
            log_folder.mkdir(parents=True, exist_ok=True)

        archive = Path(LOG_FILE)

        if archive.suffix not in (".txt", ".log"):
            archive = f"{archive}-{date}.txt"
        else:
            archive = archive.with_stem(f"{archive.stem}-{date}")

        full_path = Path(f"{log_folder}/{archive}")

        if not full_path.is_file():
            full_path.touch()

        return full_path

    def setup(self):
        """
        In this method we add the logger logic.
        return: logger(object)
        """
        path = self.verification()
        logger = logging.getLogger(self.name)
        logger.setLevel(LOG_LEVEL)
        log_format = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(filename)s | %(message)s")

        info_handler = RotatingFileHandler(
            path,
            backupCount=LOG_RETENTION
        )
        info_handler.setFormatter(log_format)
        logger.addHandler(info_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)
        logger.addHandler(stream_handler)
        return logger
