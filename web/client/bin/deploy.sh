#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER

SERVER_HOST="`jq -r '.deploy.host' < ../config.json`"
SERVER_PATH="`jq -r '.deploy.client.path' < ../config.json`"
SERVER_SERVICE="`jq -r '.deploy.client.service' < ../config.json`"

rm -rf dist
echo 'Building ...'
node_modules/.bin/webpack --config build/prod.js
echo 'Syncing ...'
rsync -arv dist/ ${SERVER_HOST}:${SERVER_PATH}
echo "Restarting ${SERVER_SERVICE} ..."
ssh ${SERVER_HOST} "sudo systemctl restart ${SERVER_SERVICE}.service"
