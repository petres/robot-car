<template>
    <div class="joystick-control m-4">
        <div class="mx-auto" :style="`position: relative; height: ${opts.outerSize}px; width: ${opts.outerSize}px`">
            <div class="rounded-full border-4" style="position: absolute; height: 100%; width: 100%; 
            background: conic-gradient(
                #FFF  22deg,
                #EEE  22deg  23deg,
                #FFF  23deg  67deg,
                #EEE  67deg  68deg, 
                #FFF  68deg 112deg,
                #EEE 112deg 113deg, 
                #FFF 113deg 157deg,
                #EEE 157deg 158deg, 
                #FFF 158deg 202deg,
                #EEE 202deg 203deg,
                #FFF 203deg 247deg,
                #EEE 247deg 248deg,
                #FFF 248deg 292deg,
                #EEE 292deg 293deg,
                #FFF 293deg 337deg,
                #EEE 337deg 338deg,
                #FFF 338deg
            );"/>
            <div ref="joy" style="position: relative; height: 100%; width: 100%;">
                <div ref="stick" class="rounded-full bg-rose-500" :style="`position: absolute; left: ${center + pos.x}px; top: ${center + pos.y}px; height: ${opts.innerSize}px; width: ${opts.innerSize}px`"></div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const opts = ref({
    innerSize: 30,
    outerSize: 250,
})

const emit = defineEmits(['status'])

const joy = ref()
const stick = ref()

const center = computed(() => opts.value.outerSize/2 - opts.value.innerSize/2)
const pos = computed(() => info.value.boundedOffset ? info.value.boundedOffset : {x: 0, y: 0})

const info = ref({
    active: false,
    // startOffset: {x: 0, y: 0},
    // currentOffset: {x: 0, y: 0}
})

const getPosFromEvent = (e) => {
    const p = joy.value.getBoundingClientRect()
    return {
        x: e.clientX - p.x - opts.value.outerSize/2,
        y: e.clientY - p.y - opts.value.outerSize/2,
    }
}

onMounted(() => {
    stick.value.addEventListener('mousedown', (e) => {
        info.value = {
            active: true,
            startOffset: getPosFromEvent(e),
        }
        // emit('status', info.value)
    }, true);

    document.addEventListener('mousemove', (e) => {
        if (info.value.active) {
            const s = opts.value.outerSize/2;

            const o = getPosFromEvent(e)

            let l = Math.sqrt(o.x**2 + o.y**2)
            let b = o
            if (l > s) {
                b = {
                    x: o.x/l*s,
                    y: o.y/l*s,
                };
                l = s
            }

            info.value.boundedOffset = b
            info.value.pos = {
                x: b.x/s,
                y: b.y/s,
                l: l/s,
            };

            emit('status', info.value)
        }
    }, true);

    document.addEventListener('mouseup', (e) => {
        if (info.value.active) {
            // console.log('stop')
            info.value = {
                active: false
            }
            emit('status', info.value)
        }
    }, true);
})

</script>
