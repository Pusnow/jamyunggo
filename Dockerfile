FROM alpine:3.10
MAINTAINER Wonsup Yoon <pusnow@me.com>

RUN apk upgrade --no-cache
RUN apk add --no-cache git python3 build-base python3-dev libffi-dev openssl-dev

COPY requirements.txt /app/

RUN pip3 install --no-cache-dir -r /app/requirements.txt


COPY jamyunggo /app/jamyunggo
COPY run.py /app/
COPY run.sh /app/
COPY config.py /app/
COPY config.json.template /config/config.json

ENV REPO ""

VOLUME ["/config", "/data"]

WORKDIR /app

CMD ["sh"]
