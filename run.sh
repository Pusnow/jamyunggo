#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d $REPO_DIR ]; then
    echo "Make dir: $REPO_DIR"

    git clone $REPO $REPO_DIR
fi

git -C $REPO_DIR pull

export PAGES="$REPO_DIR"
python3 run.py
