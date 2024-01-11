<template>
    <div class="group text-xs">
        <div class="my-2">
            <button class="mr-2" @click="connect" :disabled="store.getters.connected">Connect</button>
            <button @click="disconnect" :disabled="!store.getters.connected">Disconnect</button>
        </div>
        {{ store.state.status }}
    </div>
    <div class="text-right">
        <div>
            <img id="video" class="w-full min-h-80" :src="store.getters.stream" autoplay="autoplay" />
        </div>
        <div>
            <a class="text-xs" :href="store.getters.stream" target="_blank">{{ store.getters.stream }}</a>
        </div>
    </div>
    <div id="controls" @keyup="ku" @keydown="kd" tabindex="0">
        <div v-if="store.getters.connected">
            <div class="group">
                <div class="group-title">Move:</div>
                <button @click="s(md.rocker_move('forward', 100))" class="mr-2 text-base">↑</button>
                <button @click="s(md.rocker_move('backward', 100))" class="mr-2 text-base">↓</button>
                <button @click="s(md.rocker_move('left', 100))" class="mr-2 text-base">←</button>
                <button @click="s(md.rocker_move('right', 100))" class="mr-2 text-base">→</button>
                <button @click="s(md.rocker_move('stop', 100))" class="mr-2 text-base">⏹</button>
            </div>
            <div class="group">
                <div class="group-title">Servo:</div>
                <button @click="s(md.move_cam_servo('left'))" class="mr-2 text-base">←</button>
                <button @click="s(md.move_cam_servo('right'))" class="text-base">→</button>
            </div>
            <div class="group">
                <div class="group-title">Direct message:</div>
                <textarea v-model="message" class="p-1 w-full borrder text-xs rounded border border-slate-800 border-solid min-h-20"></textarea>
                <button @click="s(message)">Send</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
// import { useRouter, useRoute } from 'vue-router'

import { useStore } from 'vuex'
import axios from 'axios';

import * as md from '../messages.js';

const store = useStore()
const message = ref(`{
    "N": 106,
    "D1": 3
}`)

const rocker_move_keys = {
    38: 'forward',
    40: 'backward',
    37: 'left',
    39: 'right',
}

const move_cam_servo_keys = {
    65: 'left',
    83: 'right',
}

const kd = (e) => {
    console.log(`down ${e.keyCode}`)
    const k = e.keyCode
    if (k in rocker_move_keys && !e.repeat) {
        s(md.rocker_move(rocker_move_keys[k], 100))
    }
    if (k in move_cam_servo_keys && !e.repeat) {
        s(md.move_cam_servo(move_cam_servo_keys[k]))
    }
}

const ku = (e) => {
    //console.log(`up ${e.keyCode}`)
    const k = e.keyCode
    if (k in rocker_move_keys && !e.repeat) {
        s(md.rocker_move('stop', 100))
    }
}

const connect = () =>
    axios.get('/api/connect')
        .then(function (response) {
            console.log(response.data)
            document.getElementById("controls").focus();
        })

const disconnect = () => 
    axios.get('/api/disconnect')
        .then(function (response) {
            console.log(response.data)
        })

const s = (m) => {
    console.log(m)
    if (typeof m !== "string") {
        m = JSON.stringify(m)
    }
    axios.post('/api/send', { 'message': m })
        .then(function (response) {
            console.log(response.data)
        })
}
</script>
