#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER


SERVER_HOST="`jq -r '.deploy.host' < ../config.json`"
SERVER_PATH="`jq -r '.deploy.server.path' < ../config.json`"
SERVER_SERVICE="`jq -r '.deploy.server.service' < ../config.json`"

echo "${SERVER_HOST}:${SERVER_PATH}"

echo 'Syncing ...'
rsync -arv --exclude /instance --exclude '__pycache__/' --exclude '/tests' --exclude '/venv' ./ ${SERVER_HOST}:${SERVER_PATH}

echo 'Venv ...'
ssh ${SERVER_HOST} "${SERVER_PATH}/bin/venv.sh"

echo 'Restarting api server ...'
ssh ${SERVER_HOST} "systemctl --user restart ${SERVER_SERVICE}.service"
