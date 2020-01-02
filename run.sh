#!/bin/bash

cd "$(dirname "$0")"

REPO_DIR="${REPO_DIR}"
REPO="${REPO}"

if [ ! -d $REPO_DIR ]; then
    mkdir -p $REPO_DIR
    git clone $REPO $REPO_DIR
fi

git -C $REPO_DIR pull

export PAGES="$REPO_DIR"
python3 run.py
