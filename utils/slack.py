"""
This class is dedicated to send message to slack.
"""
from platform import node
from pathlib import Path
import json
import os
import requests
from utils.logger import Logger

log = Logger(__name__).setup()

class SlackNofifier():
    """
    This class is responsible for simplifying slack messages.
    Attributes:
        slack_webhook_url: URL that will be used to make the post call.
        file_name: Name of the temporary file that will be used to send messages to Slack.
    """
    def __init__(self, slack_webhook_url: str, file_name: str):
        self.slack_webhook_url = slack_webhook_url
        self.file_name = file_name

    def setup(self):
        """
        This function is responsible for preparing the necessary actions 
        to be able to send messages to Slack.
        """
        filename = Path(self.file_name).absolute()
        # Check if file exists
        if not filename.exists():
            filename.touch()
            log.info("Creating a json file")

        base = ({
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": f"Server: {node()}"
                    }
                }
            ]
        })
        if filename.stat().st_size == 0:
            log.info("Adding base json data.")
            with open(self.file_name, "r+", encoding="utf-8") as _file:
                json.dump(base, _file, indent=4)


    def write_message(self, message: str):
        """
        This method is responsible for writing the messages in a json file 
        that will end up being sent to Slack.
        Params:
            message (str):
        """
        self.setup()

        data = ({
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": f"{message}",
                "emoji": True
            }
        })

        with open(self.file_name, "r+", encoding="utf-8") as _file:
            file_data = json.load(_file)
            file_data["blocks"].append(data)
            _file.seek(0)
            json.dump(file_data, _file, indent=4)
            log.info("Writing a message to send to slack.")

    def send_message(self):
        """
        Send message to slack.
        """
        _file = open(self.file_name, "r+", encoding="utf-8")
        if _file.mode == "r+":
            payload = json.load(_file)
        requests.post(self.slack_webhook_url, json=payload, timeout=10)
        os.remove(self.file_name)
        log.info("Sent message to slack.")
