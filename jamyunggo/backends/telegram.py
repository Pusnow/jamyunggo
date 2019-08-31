import bleach
from bs4 import BeautifulSoup

import telegram
from config import config

if config["TELEGRAM"]["ENABLED"]:
    BOT = telegram.Bot(token=config["TELEGRAM"]["TOKEN"])
    USER_WHITELIST = set([a.lower() for a in config["TELEGRAM"]["WHITELIST"]])
    CHAT_SET = set(config["TELEGRAM"]["CHAT_ID"])
    for update in BOT.get_updates():
        if update['message']['chat']['username'].lower() in USER_WHITELIST:
            CHAT_SET.add(update['message']['chat']['id'])

    with open(config["TELEGRAM"]["CONFIG"], "w") as telegram_last:
        telegram_last.write("\n".join([str(id) for id in CHAT_SET]))


def notify(module_name, title, text=None, url=None, name=None):
    if not config["TELEGRAM"]["ENABLED"]:
        return False
    if name:
        text_msg = "<b>[%s]%s</b>\n" % (name, title.replace(
            "<", "&lt").replace(">", "&gt").replace("&", "&amp"))
    else:
        text_msg = "<b>%s</b>\n" % title.replace("<", "&lt").replace(
            ">", "&gt").replace("&", "&amp")
    img_urls = []
    if url:
        text_msg += '<a href="%s">%s</a>\n' % (url, url.replace(
            "<", "&lt").replace(">", "&gt").replace("&", "&amp"))
    # Telegram Skip message
    #text_msg += bleach.clean(text, tags=['a','b','i','strong','code','pre'], strip=True)[:200]

    # TODO: Fix photo timeout bug
    #soup = BeautifulSoup(text, 'html.parser')
    #for img in soup.find_all("img"):
    #        img_urls.append(img["src"])

    for chat_id in CHAT_SET:
        BOT.send_message(chat_id, text_msg, parse_mode="HTML")
    #    for img_url in img_urls:
    #        BOT.send_photo(chat_id, img_url,  disable_notification=True, timeout=60)

    return True
