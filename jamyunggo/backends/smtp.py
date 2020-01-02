import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from config import config

NAME = "SMTP"


def notify(module_name, title, text=None, url=None, name=None):
    with smtplib.SMTP_SSL(config["SMTP"]["SERVER"]) as s:
        s.login(config["SMTP"]["ID"], config["SMTP"]["PW"])

        html = "<h2>%s</h2>" % title
        if url:
            html += '<a href="%s">%s</a>' % (url, url)

        if text:
            html += text

        html = html.replace("\n", "")
        msg = MIMEMultipart('alternative')

        for receivor in config["SMTP"]["RECEIVERS"]:
            if name:
                msg['Subject'] = "[" + name + "] " + title
            else:
                msg['Subject'] = "[" + module_name + "] " + title
            msg['From'] = formataddr(
                (str(Header("Jamyunggo", 'utf-8')), config["SMTP"]["ID"]))
            msg['To'] = receivor

            msg.attach(MIMEText(html, "html"))
            s.sendmail(config["SMTP"]["ID"], receivor, msg.as_string())
        s.quit()

    return True
