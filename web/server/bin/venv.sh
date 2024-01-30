#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER

[ ! -d "./venv" ] && echo "Creating virual environment" && python -m venv venv

. ./venv/bin/activate
pip install -r requirements.txt
