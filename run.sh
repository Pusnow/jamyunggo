#!/bin/sh

GIT_DIR=/app/pages
GIT_REPO="${REPO}"

if [ ! -d $GIT_DIR ]
then
    git clone $GIT_REPO  $GIT_DIR
fi

git -C $GIT_DIR pull

cd /app
JAMYUNGGO_CONFIG=/app/config.json python3 run.py