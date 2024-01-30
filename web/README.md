# web interface

as replacement for the (closed source) mobile app, we implemented a simple 
web interface for controlling the robot car. only this part of the repo can
be licensed and is lincensed under the license GNU GPLv3.



## client (frontend)

stack: js, webpack, vue, tailwind

### install

``` {bash}
cd client
npm install
```


### run

``` {bash}
npm run dev
```

## server (backend)

stack: python, flask

the server sends after connecting heartbeats to the robot. for this (and other) messages,
like in the original firmware, an invalid json format is used. 
two threads are used for communication, one for sending, one for receiving 
messages. another thread reads the webcam.


### install

We are using virtual envirements, so:

``` {bash}
cd server
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

adjust the file `server/instance/config.json` to your needs.

### run

#### dev
```
./server/bin/flask.sh
```

#### prod
```
./server/bin/gunicorn.sh
```
