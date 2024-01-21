<template>
    <router-view v-slot="{ Component }" v-if="store.getters.initialized">
        <component :is="Component" />
    </router-view>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";

import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()

const doPolling = () => {
    store.commit('status')
    setTimeout(doPolling, 2000)
}
doPolling()

onMounted(() => {
    store.commit('init')
});
</script>
