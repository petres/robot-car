<template>
    <div v-if="store.getters.initialized">
        <div class="inner">
            <router-view v-slot="{ Component }">
                <component :is="Component" />
            </router-view>
        </div>
    </div>
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
