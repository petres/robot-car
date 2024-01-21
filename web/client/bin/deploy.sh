#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER

rm -rf dist
echo 'Building ...'
node_modules/.bin/webpack --config build/prod.js
echo 'Syncing ...'
rsync -arv dist/ peter@zeros.home:/home/peter/elegoo/client

ssh peter@zeros.home "sudo systemctl restart nginx.service"
