#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER

rm -rf dist
echo 'Building ...'
node_modules/.bin/webpack --config build/prod.js
echo 'Syncing ...'
rsync -e 'ssh -p 23322' -arv dist/ --exclude '/assets/data/*' petres@explorer100.abteil.org:/var/www/vienna/web
