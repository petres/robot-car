<template>
    <div class="container mx-full my-2 mx-auto max-w-md" v-if="store.getters.initialized">
        <router-view v-slot="{ Component }">
            <component :is="Component" />
        </router-view>
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
