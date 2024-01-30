<template>
    <div style="background-color: black;" @keyup="ku" @keydown="kd" tabindex="0">
        <div class="flex h-screen">
            <div class="m-auto">
                <!-- <img id="video" class="max-w-screen max-h-screen m-auto" style="transform: rotate(180deg);" :src="store.getters.stream" autoplay="autoplay"/> -->
                <img id="video" class="max-w-screen max-h-screen m-auto" style="transform: rotate(180deg);" src="/api/stream" autoplay="autoplay"/>
            </div>
        </div>
        <joystick-control @status="joystick" style="position: fixed; bottom: 10px; right: 10px"/>
        <div style="position: fixed; bottom: 10px; left: 10px">
            <button @click="r.send(md.move_cam_servo('left'))" class="text-base bg-red mr-2">←</button>
            <button @click="r.send(md.set_cam_servo(90))" class="text-base bg-red mr-2">|</button>
            <button @click="r.send(md.move_cam_servo('right'))" class="text-base bg-red">→</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';

import * as md from '../messages.js';
import * as r from '../robot.js';

const store = useStore()

import JoystickControl from '../JoystickControl.vue';

const speed = ref(80)
const maxSpeed = 150

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


let lastSentJoystickEvent = Date.now();
const joystick = (status) => {
    if (status.active) {
        const n = Date.now();
        if ((n - lastSentJoystickEvent > 80)) {
            const pos = status.pos
            const speed = pos.l * maxSpeed;
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

onMounted(() => {
    r.connect()
});

</script>
