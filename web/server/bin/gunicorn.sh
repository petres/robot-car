#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER

. venv/bin/activate
gunicorn --workers 1 --threads 10 "api:app" --timeout 0 --bind 127.0.0.1:8888

