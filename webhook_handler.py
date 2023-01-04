"""webhook_handler.py
Replaces discord_integration.py.
Handles the sending of messages and images to Discord via
webhooks.

Thanks to Bals2oo8 for giving me a hand with getting
file sending working.
"""
import json
import requests
import datetime

from gph_config import *
from gph_logging import log_message

if TEST_MODE:
    wh_url = TEST_WEBHOOK
else:
    wh_url = WEBHOOK


class WebhookHandler:
    _files = {}
    webhook_data = {}
    embeds = {}

    def __init__(self, hook_url=None):
        self._files = {}
        self.webhook_data = {}
        self.embeds = []
        self.wh_url = wh_url
        self.hook_url = hook_url

    def add_file(self, file: bytes, filename: str) -> None:
        self._files[f"_{filename}"] = (filename, file)

    def config_webhook(self, content: str, username: str) -> None:
        self.webhook_data["content"] = content
        self.webhook_data["username"] = username
        self.webhook_data["embeds"] = self.embeds

    def make_post_request(self, url: str, data: dict, _files: dict) -> requests.post:
        if not bool(self._files):
            return requests.post(url, json=data)

        self._files["payload_json"] = (None, json.dumps(data))
        return requests.post(url, files=self._files)

    def send_message(self, msg: str, name=BOT_NAME, avatar=AVATAR_URL) -> None:
        self.config_webhook(msg, name)
        self.webhook_data["avatar_url"] = avatar
        if self.hook_url is not None:
            self.wh_url = self.hook_url
        response = self.make_post_request(self.wh_url, self.webhook_data, self._files)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            log_message(err)
        else:
            now = datetime.datetime.now()
            timestamp = now.strftime('%d %b %Y - %H:%M:%S ')
            log_message(f'Text payload delivered with code {response.status_code} '
                        f'at {timestamp}', log=LOG_NAME)
            print(f'Text payload delivered with code {response.status_code} '
                  f'at {timestamp}')
            self.webhook_data = {}
            self._files = {}

    def send_embed(self, msg: str, embeds: list, name=BOT_NAME, avatar=AVATAR_URL) -> None:
        self.config_webhook(msg, name)
        self.webhook_data["avatar_url"] = avatar
        self.webhook_data["embeds"] = embeds
        if self.hook_url is not None:
            self.wh_url = self.hook_url
        response = self.make_post_request(self.wh_url, self.webhook_data, self._files)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            log_message(err)
        else:
            now = datetime.datetime.now()
            timestamp = now.strftime('%d %b %Y - %H:%M:%S ')
            log_message(f'Text payload delivered with code {response.status_code} '
                        f'at {timestamp}', log=LOG_NAME)
            print(f'Text payload delivered with code {response.status_code} '
                  f'at {timestamp}')
            self.webhook_data = {}
            self._files = {}

    def send_file(self, msg: str, filename: str, name=BOT_NAME, avatar=AVATAR_URL) -> None:
        self.config_webhook(msg, name)
        self.webhook_data["avatar_url"] = avatar
        fdata = open(filename, 'rb')
        self.add_file(fdata, filename)
        if self.hook_url is not None:
            self.wh_url = self.hook_url
        response = self.make_post_request(self.wh_url, self.webhook_data, self._files)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            log_message(err)
        else:
            now = datetime.datetime.now()
            timestamp = now.strftime('%d %b %Y - %H:%M:%S ')
            log_message(f'File payload delivered with code {response.status_code}'
                        f' at {timestamp}', log=LOG_NAME)
            print(f'File payload delivered with code {response.status_code}'
                  f' at {timestamp}')
        fdata.close()
        self.webhook_data = {}
        self._files = {}
