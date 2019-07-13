#!/bin/sh

GIT_DIR=/app/pages
GIT_REPO=

if [ ! -d $GIT_DIR ]
then
    git clone $GIT_REPO  $GIT_DIR
fi

git -C $GIT_DIR pull

cd /app
JAMYUNGGO_CONFIG=/config/config.json python3 run.py