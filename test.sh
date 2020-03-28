#!/bin/bash

export CACHE_DIR="data/cache/"

export REPO_DIR="data/pages/"
export REPO=""

export GMAIL_ENABLED=0
export GMAIL_ID=""
export GMAIL_PW=""
export GMAIL_RECEIVERS=""

export SMTP_ENABLED=0
export SMTP_SERVER=""
export SMTP_ID=""
export SMTP_PW=""
export SMTP_RECEIVERS=""

export TELEGRAM_ENABLED=0
export TELEGRAM_TOKEN=""
export TELEGRAM_WHITELIST=""
export TELEGRAM_CHAT_ID=""
export TELEGRAM_CONFIG=""

export NEXTCLOUD_ENABLED=0
export NEXTCLOUD_HOST=""
export NEXTCLOUD_ID=""
export NEXTCLOUD_PW=""
export NEXTCLOUD_TO=""

export DUMMY_ENABLED=0
./run.sh
