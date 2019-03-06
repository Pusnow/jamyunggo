"""
Example EZone (IITP)

"""
import re
import urllib
BACKENDS = ["telegram"]

NAME = "IITP 공고"
URL = "https://ezone.iitp.kr/common/anno/list"
FIND_ALL_ARGS = {"class_": "bbs_cnt"}

HEADERS = {}


def TITLE_FN(node):
    return node.find_all("span", class_="tit")[0].get_text().strip()


def BODY_URL_FN(node):
    return re.sub(r"jsessionid=.*?tomcat[0-9]", "",
                  node.find_all("a")[0]["href"])


def BODY_FN(soup):
    result = soup.find_all(class_="bbs_view_cnt")
    if result:
        return result[0]
    else:
        return None


def PARAM_FN(node):
    url = BODY_URL_FN(node)
    attr = "query"
    param = getattr(urllib.parse.urlsplit(url), attr)
    return param