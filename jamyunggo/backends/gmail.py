import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import config


def notify(module_name, title, text=None, url=None, name=None):

    with smtplib.SMTP_SSL('smtp.gmail.com') as s:
        s.login(config["GMAIL"]["ID"], config["GMAIL"]["PW"])

        html = "<h2>%s</h2>" % title
        if url:
            html += '<a href="%s">%s</a>' % (url, url)

        if text:
            html += text

        html = html.replace("\n", "")
        msg = MIMEMultipart('alternative')

        for receivor in config["GMAIL"]["GMAIL_RECEIVERS"]:
            if name:
                msg['Subject'] = "[" + name + "] " + title
            else:
                msg['Subject'] = "[" + module_name + "] " + title
            msg['From'] = "Jamyunggo"
            msg['To'] = receivor

            msg.attach(MIMEText(html, "html"))
            s.sendmail(config["GMAIL"]["ID"], receivor, msg.as_string())
        s.quit()

    return True
