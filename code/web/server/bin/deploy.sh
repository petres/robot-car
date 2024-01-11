#!/usr/bin/env bash

BASE_FOLDER=`dirname -- "$0"`/..;
cd $BASE_FOLDER

rsync -arv --exclude /instance --exclude '__pycache__/' --exclude '/tests' --exclude '/venv' ./ peter@zeros.home:/home/peter/elegoo/server

# ssh -p 23322 petres@explorer100.abteil.org "/var/www/vienna/server/bin/venv.sh"
ssh peter@zeros.home "sudo systemctl restart elegoo-api-server"
