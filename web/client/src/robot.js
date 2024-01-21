import axios from 'axios';

const connect = () =>
    axios.get('/api/connect')
        .then(function (response) {
            // console.log(response.data)
            // document.getElementById("controls").focus();
        })

const disconnect = () => 
    axios.get('/api/disconnect')
        .then(function (response) {
            // console.log(response.data)
        })

const send = (m) => {
    console.log(m)
    if (typeof m !== "string") {
        m = JSON.stringify(m)
    }
    axios.post('/api/send', { 'message': m })
        .then(function (response) {
            // console.log(response.data)
        })
}


export {
    connect,
    disconnect,
    send,
}