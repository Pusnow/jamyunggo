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
        text_msg = "[%s]%s\n" % (name, title.replace("<", "&lt").replace(
            ">", "&gt").replace("&", "&amp"))
    else:
        text_msg = "%s\n" % title.replace("<", "&lt").replace(
            ">", "&gt").replace("&", "&amp")
    if url:
        text_msg += '%s\n' % url.replace("<", "&lt").replace(
            ">", "&gt").replace("&", "&amp")

    webhook_url = config["SLACK"]["WEBHOOK"]
    session.post(webhook_url, json={
        "text": text_msg,
    })
    return True
