from urllib.parse import urljoin

import requests

from config import config

NAME = "SLACK"
TOKEN = {}
session = requests.Session()


def notify(module_name, title, text=None, url=None, name=None):
    if "SLACK" not in config:
        return False

    if not config["SLACK"]["WEBHOOK"]:
        return False
    if name:
        text_msg = "[%s]%s\n" % (name, title)
    else:
        text_msg = "%s\n" % title
    if url:
        text_msg += '%s\n' % url

    webhook_url = config["SLACK"]["WEBHOOK"]
    session.post(webhook_url, json={
        "text": text_msg,
    })
    return True
