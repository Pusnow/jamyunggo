import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def notify(module_name, title, text=None, url=None):

    with smtplib.SMTP_SSL(config.SMTP_SERVER) as s:
        s.login(config.SMTP_ID, config.SMTP_PW)

        html = "<h2>%s</h2>" % title
        if url:
            html += '<a href="%s">%s</a>' % (url, url)

        if text:
            html += text

        html = html.replace("\n", "")
        msg = MIMEMultipart('alternative')

        for receivor in config.SMTP_RECEIVERS:
            msg['Subject'] = "[" + module_name + "] " + title
            msg['From'] = "Jamyunggo"
            msg['To'] = receivor

            msg.attach(MIMEText(html, "html"))
            s.sendmail(config.GMAIL_ID, receivor, msg.as_string())
        s.quit()

    return True
