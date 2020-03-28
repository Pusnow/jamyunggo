from urllib.parse import urljoin

import requests

from config import config

NAME = "NEXTCLOUD"
TOKEN = {}
headers = {
    'OCS-APIRequest': 'true',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
session = requests.Session()
if "NEXTCLOUD" in config:
    NEXT_HOST = config["NEXTCLOUD"]["HOST"]
    NEXT_ID = config["NEXTCLOUD"]["ID"]
    NEXT_PW = config["NEXTCLOUD"]["PW"]
    NEXT_TO = config["NEXTCLOUD"]["TO"]

    ENDPOINT = urljoin(NEXT_HOST, "/ocs/v2.php/apps/spreed/api/v1/")
    ROOM = urljoin(ENDPOINT, "room")

    resp = session.get(ROOM, headers=headers, auth=(NEXT_ID, NEXT_PW))
    for talk in resp.json()["ocs"]["data"]:
        if talk["type"] != 1:
            continue
        if talk["name"] in NEXT_TO:
            TOKEN[talk["name"]] = talk["token"]
    for name in NEXT_TO:
        if name in TOKEN:
            continue
        try:
            resp = session.post(ROOM,
                                json={
                                    "roomType": 1,
                                    "invite": name
                                },
                                headers=headers,
                                auth=(NEXT_ID, NEXT_PW))
            TOKEN[name] = resp.json()["ocs"]["data"]["token"]
        except:
            print(name, "failed")


def notify(module_name, title, text=None, url=None, name=None):
    CHAT = urljoin(ENDPOINT, "chat/")
    if name:
        text_msg = "[%s]%s\n" % (name, title.replace("<", "&lt").replace(
            ">", "&gt").replace("&", "&amp"))
    else:
        text_msg = "%s\n" % title.replace("<", "&lt").replace(
            ">", "&gt").replace("&", "&amp")
    if url:
        text_msg += '%s\n' % url.replace("<", "&lt").replace(
            ">", "&gt").replace("&", "&amp")

    for to in TOKEN:
        chat_url = urljoin(CHAT, TOKEN[to])
        resp = session.post(chat_url,
                            json={
                                "message": text_msg,
                            },
                            headers=headers,
                            auth=(NEXT_ID, NEXT_PW))
    return True
