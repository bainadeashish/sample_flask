#!/bin/sh

python log-generator.py --path /data/miniodata/logs --days 5 --lines 500 --files 3
python -u  manage.py startserver 2>&1 >/python.log & tail -f /python.log & celery -A app.tasks:celery worker --loglevel=DEBUG


