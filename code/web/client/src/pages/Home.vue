<template>
    <img id="video" :src="store.getters.stream" autoplay="autoplay" />
    <div>
        <a :href="store.getters.stream" target="_blank">{{ store.getters.stream }}</a>
    </div>
    <div>
        {{ store.state.status }}
        <button @click="connect" :disabled="store.getters.connected">Connect</button>
        <button @click="disconnect" :disabled="!store.getters.connected">Disconnect</button>
        <div>
            <textarea v-model="message"></textarea>
        </div>
        <button @click="send" :disabled="!store.getters.connected">Send</button>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
// import { useRouter, useRoute } from 'vue-router'

import { useStore } from 'vuex'
import axios from 'axios';

const store = useStore()
const message = ref("abc")

const connect = () => 
    axios.get('/api/connect')
        .then(function (response) {
            console.log(response.data)
        })

const disconnect = () => 
    axios.get('/api/disconnect')
        .then(function (response) {
            console.log(response.data)
        })

const send = () => 
    axios.post('/api/send', { 'message': message.value })
        .then(function (response) {
            console.log(response.data)
        })


const bounds_map = computed(() => {
})

onMounted(() => {
   
});
</script>
