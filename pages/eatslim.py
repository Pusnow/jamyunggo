"""
Example Eatslim

"""
import re
BACKENDS = ["telegram"]

NAME = "잇슬림"
URL = "http://www.eatsslim.co.kr/mobile/event/index.jsp"
FIND_ALL_ARGS = {"class_": "info"}

HEADERS = {}


def TITLE_FN(node):
    return node.find_all("p", class_="title")[0].get_text().strip()


def BODY_URL_FN(node):
    return node.find_previous_siblings(
        "div", class_="img")[0].find_all("a")[0]["href"]


def BODY_FN(soup):
    result = soup.find_all(class_="article")
    if result:
        return result[0]
    else:
        return None