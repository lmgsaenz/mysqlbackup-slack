"""
This script is in charge of defining and loading the environment 
variables of the operating system and establishing some default values.
"""
from decouple import config, Csv

LOG_FOLDER = config("LOG_FOLDER")
LOG_FILE = config("LOG_FILE")
LOG_LEVEL = config("LOG_LEVEL")
LOG_RETENTION = config("LOG_RETENTION")
BACKUP_FOLDER = config("BACKUP_FOLDER")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DATABASES = config("DATABASES", cast=Csv(post_process=list, strip="[]", delimiter=','))
SLACK_WEBHOOK_URL = config("SLACK_WEBHOOK_URL")
SLACK_FILENAME = config("SLACK_FILENAME")
