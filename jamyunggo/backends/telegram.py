import config
import telegram


BOT = telegram.Bot(token = config.TELEGRAM_TOKEN)
USER_WHITELIST = set([a.lower() for a in config.TELEGRAM_WHITELIST])
CHAT_SET = set()
for update in BOT.get_updates():
    if update['message']['chat']['username'].lower() in USER_WHITELIST:
        CHAT_SET.add(update['message']['chat']['id'])


def notify(module_name, title, text=None, url=None):
    html = "<h2>%s</h2>" % title
    if url:
        html += '<a href="%s">%s</a>' % (url, url)

    if text:
        html += text


    for chat_id in CHAT_SET:
        bot.send_message(chat_id, html, parse_mode="HTML")
    return True
