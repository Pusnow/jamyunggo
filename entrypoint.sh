#!/bin/sh

echo "*/15 * * * * /app/run.sh" | crontab - && crond -f -L /dev/stdout