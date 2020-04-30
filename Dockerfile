FROM debian:buster-slim
MAINTAINER Wonsup Yoon <pusnow@me.com>

RUN cd /etc/apt && \
    sed -i 's/deb.debian.org/mirror.kakao.com/g' sources.list

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    build-essential \
    python3-dev \
    python3-pip \
    python3-dateutil \
    ssh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


COPY requirements.txt /app/

RUN pip3 install --no-cache-dir -r /app/requirements.txt


COPY jamyunggo /app/jamyunggo
COPY run.py /app/
COPY run.sh /app/
COPY config.py /app/

ENV CACHE_DIR "data/cache/"
ENV REPO_DIR "data/pages/"
ENV REPO ""

ENV GMAIL_ENABLED "0"
ENV GMAIL_ID ""
ENV GMAIL_PW ""
ENV GMAIL_RECEIVERS ""

ENV SMTP_ENABLED "0"
ENV SMTP_SERVER ""
ENV SMTP_ID ""
ENV SMTP_PW ""
ENV SMTP_RECEIVERS ""

ENV TELEGRAM_ENABLED "0"
ENV TELEGRAM_TOKEN ""
ENV TELEGRAM_WHITELIST ""
ENV TELEGRAM_CHAT_ID ""
ENV TELEGRAM_CONFIG ""

ENV NEXTCLOUD_ENABLED "0"
ENV NEXTCLOUD_HOST ""
ENV NEXTCLOUD_ID ""
ENV NEXTCLOUD_PW ""
ENV NEXTCLOUD_TO ""

ENV SLACK_ENABLED "0"
ENV SLACK_WEBHOOK ""

ENV DUMMY_ENABLED "0"

VOLUME ["/app/data"]

WORKDIR /app

CMD  ["/app/run.sh"]