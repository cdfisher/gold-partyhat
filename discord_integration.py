"""discord_integration.py
Handles sending of messages to Discord via webhooks.
"""

import requests
import datetime

from gph_config import *
from gph_logging import log_message

# Handles quick switching between sending messages to the Discord test server
# and to the production server.
if TEST_MODE:
    WH = TEST_WEBHOOK
else:
    WH = WEBHOOK


def send_message(message):
    """Send text message to Discord.
    :param message: Text of the message to send. Length <= 2000 characters.
    :return: Prints status code or HTTP error to console.
    """

    # Build JSON payload to send to Discord server
    data = {
        'content': message,
        'username': BOT_NAME   # Set in gph_config.py, overridden by setting in server
    }

    result = requests.post(WH, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        timestamp = datetime.datetime.now()
        log_message('Payload delivered with code {} at {}'.format(result.status_code, timestamp))


# TODO Implement image sending once data graphing is implemented
def send_image(message, file):
    """Send image and text message to Discord.

    :param message: Text of the message to send. Length <= 2000 characters.
    :param file: Image to send in message.
    :return: Prints status code or HTTP error to console.
    """
    return
