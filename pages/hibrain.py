"""
Example Hibrain Resarch

"""
import re
BACKENDS = ["telegram"]

NAME = "Hibrain 연구비지원"
URL = "https://www.hibrain.net/research/researches/34/recruitments/108/recruits?sortType=AD&displayType=TIT&listType=ING&limit=25&siteid=1"
FIND_ALL_ARGS = {"class_": "listTypeRecruit"}
PARAM = "JMG_PATH"

HEADERS = {}


def TITLE_FN(node):
    return node.find_all("span", class_="title")[0].get_text().strip()


def BODY_URL_FN(node):
    return node.find_all("a")[0]["href"]


def BODY_FN(soup):
    return None