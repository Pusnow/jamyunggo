FROM alpine:3.10
MAINTAINER Wonsup Yoon <pusnow@me.com>

RUN apk upgrade --no-cache
RUN apk add --no-cache git python3 build-base python3-dev libffi-dev openssl-dev openssh

COPY requirements.txt /app/

RUN pip3 install --no-cache-dir -r /app/requirements.txt


COPY jamyunggo /app/jamyunggo
COPY run.py /app/
COPY run.sh /app/
COPY config.py /app/

ENV REPO ""

VOLUME ["/data"]

WORKDIR /app

COPY        entrypoint.sh /
RUN         chmod +x /entrypoint.sh
ENTRYPOINT  ["/entrypoint.sh"]
