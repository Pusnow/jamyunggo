import json
import os

config = {}

config["CACHE_DIR"] = os.environ['CACHE_DIR'].strip()
config["PAGES"] = [repo.strip() for repo in os.environ['PAGES'].split(",")]

if int(os.environ['GMAIL_ENABLED']) == 1:
    config["GMAIL"] = {}
    config["GMAIL"]["ID"] = os.environ['GMAIL_ID'].strip()
    config["GMAIL"]["PW"] = os.environ['GMAIL_PW'].strip()
    config["GMAIL"]["RECEIVERS"] = [
        receiver.strip()
        for receiver in os.environ['GMAIL_RECEIVERS'].split(",")
    ]

if int(os.environ['SMTP_ENABLED']) == 1:
    config["SMTP"] = {}
    config["SMTP"]["SERVER"] = os.environ['SMTP_SERVER'].strip()
    config["SMTP"]["ID"] = os.environ['SMTP_ID'].strip()
    config["SMTP"]["PW"] = os.environ['SMTP_PW'].strip()
    config["SMTP"]["RECEIVERS"] = [
        receiver.strip()
        for receiver in os.environ['SMTP_RECEIVERS'].split(",")
    ]

if int(os.environ['TELEGRAM_ENABLED']) == 1:
    config["TELEGRAM"] = {}
    config["TELEGRAM"]["TOKEN"] = os.environ['TELEGRAM_TOKEN'].strip()
    config["TELEGRAM"]["WHITELIST"] = [
        whitelist.strip()
        for whitelist in os.environ['TELEGRAM_WHITELIST'].split(",")
    ]

    config["TELEGRAM"]["CHAT_ID"] = [
        chatid.strip() for chatid in os.environ['TELEGRAM_CHAT_ID'].split(",")
    ]
    config["TELEGRAM"]["CONFIG"] = os.environ['TELEGRAM_CONFIG'].strip()

if int(os.environ['DUMMY_ENABLED']) == 1:
    config["DUMMY"] = {}
