#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER

. venv/bin/activate
python ./venv/bin/flask --app api --debug run -h 0.0.0.0 -p 8888
