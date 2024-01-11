import { createStore } from 'vuex'

import axios from 'axios';

// import * as api from '@/shared/api.js'

const store = createStore({
    devtools: false,
    state: () => ({
        config: null,
        status: null,
    }),
    getters: {
        initialized (state) {
            return state.config !== null
        },
        connected (state) {
            return state.status && state.status.is_alive
        },
        stream (state, getters) {
            return `http://${state.config.host}:${state.config.stream.port}/${state.config.stream.path}`
        }
    },
    mutations: {
        init(state) {
            axios.get('/api/config')
                .then(function (response) {
                    state.config = response.data
                })
        },
        status(state) {
            axios.get('/api/status')
                .then(function (response) {
                    state.status = response.data
                })
        }
    }
})

export {
    store
}
