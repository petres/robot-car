<template>
    <div class="container mx-full my-2 mx-auto max-w-md">
        <div class="group text-xs">
            <div class="my-2">
                <button class="mr-2" @click="r.connect" :disabled="store.getters.connected">Connect</button>
                <button @click="r.disconnect" :disabled="!store.getters.connected">Disconnect</button>
            </div>
            {{ store.state.status }}
        </div>
        <div class="text-right">
            <div>
                <!-- <img id="video" class="w-full min-h-80" :src="store.getters.stream" autoplay="autoplay" /> -->
                <img id="video" class="w-full min-h-80" src="/api/stream" autoplay="autoplay" />
            </div>
            <div>
                <a class="text-xs" :href="store.getters.stream" target="_blank">{{ store.getters.stream }}</a>
            </div>
        </div>
        <div>
            <div id="controls" @keyup="ku" @keydown="kd" tabindex="0">
            <!-- <div v-if="store.getters.connected"> -->
                <div class="group">
                    <div class="group-title">Move:</div>
                    <joystick-control class="mx-auto m-4 bg-black p-2" @status="joystick"/>
                    <div class="buttons">
                        <button @click="r.send(md.rocker_move('forward', speed))" class="mr-2 text-base">↑</button>
                        <button @click="r.send(md.rocker_move('backward', speed))" class="mr-2 text-base">↓</button>
                        <button @click="r.send(md.rocker_move('left', speed))" class="mr-2 text-base">←</button>
                        <button @click="r.send(md.rocker_move('right', speed))" class="mr-2 text-base">→</button>
                        <button @click="r.send(md.rocker_move('stop', 0))" class="mr-2 text-base">⏹</button>
                        <input v-model="speed" type="range" :min=0 max=250 value=70 class="slider" />
                    </div>
                    <!-- <div>
                        <div id="joystick" class="mx-auto" style="height: 200px; width: 200px;"/>
                    </div> -->
                </div>
                <div class="group">
                    <div class="group-title">Servo:</div>
                    <button @click="r.send(md.move_cam_servo('left'))" class="mr-2 text-base">←</button>
                    <button @click="r.send(md.set_cam_servo(90))" class="mr-2 text-base">|</button>
                    <button @click="r.send(md.move_cam_servo('right'))" class="text-base">→</button>
                </div>

            </div>
            <div class="group">
                <div class="group-title">Direct message:</div>
                <textarea v-model="message" class="p-1 w-full borrder text-xs rounded border border-slate-800 border-solid min-h-20"></textarea>
                <button @click="r.send(message)">Send</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
// import { useRouter, useRoute } from 'vue-router'

import { useStore } from 'vuex'
import JoystickControl from '../JoystickControl.vue';

import * as md from '../messages.js';
import * as r from '../robot.js';

const store = useStore()
const message = ref(`{
    "N": 106,
    "D1": 3
}`)
const speed = ref(100)

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

let lastSentJoystickEvent = Date.now();
const joystick = (status) => {
    if (status.active) {
        const n = Date.now();
        if ((n - lastSentJoystickEvent > 80)) {
            const pos = status.pos
            const speed = pos.l * 250;
            const angle = Math.atan2(pos.x, -pos.y);

            const fb = Math.abs(angle) < Math.PI/2 ? "forward" : "backward";
            const rl = angle > 0 ? "right" : "left";
            const p = Math.round(Math.abs(angle)/(Math.PI/4))

            let dir = null
            if ([0, 4].includes(p)) {
                dir = fb
            } else if (p == 2) {
                dir = rl
            } else {
                dir = `${rl}${fb.charAt(0).toUpperCase() + fb.slice(1)}`
            }
            // console.log({
            //     speed, dir
            // })
            r.send(md.rocker_move(dir, Math.round(speed)));
            lastSentJoystickEvent = n;
        }
    } else {
        r.send(md.rocker_move("stop", 0));
    }
} 

const kd = (e) => {
    // console.log(`down ${e.keyCode}`)
    const k = e.keyCode
    if (k in rocker_move_keys && !e.repeat) {
        r.send(md.rocker_move(rocker_move_keys[k], +speed.value))
    }
    if (k in move_cam_servo_keys && !e.repeat) {
        r.send(md.move_cam_servo(move_cam_servo_keys[k]))
    }
}

const ku = (e) => {
    //console.log(`up ${e.keyCode}`)
    const k = e.keyCode
    if (k in rocker_move_keys && !e.repeat) {
        r.send(md.rocker_move('stop', 0))
    }
}

</script>
