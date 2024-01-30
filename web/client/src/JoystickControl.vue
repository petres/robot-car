<template>
    <div class="joystick-control">
        <div class="mx-auto" :style="`touch-action: none; position: relative; height: ${opts.outerSize}px; width: ${opts.outerSize}px`">
            <div class="rounded-full border-4" style="border-color: #EEEEEE22; position: absolute; height: 100%; width: 100%; 
            background: conic-gradient(
                #FFFFFF11  22deg,
                #EEEEEE33  22deg  23deg,
                #FFFFFF11  23deg  67deg,
                #EEEEEE33  67deg  68deg, 
                #FFFFFF11  68deg 112deg,
                #EEEEEE33 112deg 113deg, 
                #FFFFFF11 113deg 157deg,
                #EEEEEE33 157deg 158deg, 
                #FFFFFF11 158deg 202deg,
                #EEEEEE33 202deg 203deg,
                #FFFFFF11 203deg 247deg,
                #EEEEEE33 247deg 248deg,
                #FFFFFF11 248deg 292deg,
                #EEEEEE33 292deg 293deg,
                #FFFFFF11 293deg 337deg,
                #EEEEEE33 337deg 338deg,
                #FFFFFF11 338deg
            );"/>
            <div ref="joy" style="position: relative; height: 100%; width: 100%;">
                <div ref="stick" class="rounded-full bg-red" :style="`position: absolute; left: ${center + pos.x}px; top: ${center + pos.y}px; height: ${opts.innerSize}px; width: ${opts.innerSize}px`"></div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const opts = ref({
    innerSize: 40,
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
    const t = e.clientX ? e : e.touches[0]
    const p = joy.value.getBoundingClientRect()
    return {
        x: t.clientX - p.x - opts.value.outerSize/2,
        y: t.clientY - p.y - opts.value.outerSize/2,
    }
}

const onStart = (e) => {
    if (!info.value.active) {
        info.value = {
            active: true,
            startOffset: getPosFromEvent(e),
        }
        e.preventDefault()
    }
    // emit('status', info.value)
};

const onMove = (e) => {
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

        e.preventDefault()
        emit('status', info.value)
    }
}

const onEnd = (e) => {
    if (info.value.active) {
        // console.log('stop')
        info.value = {
            active: false
        }
        
        e.preventDefault()
        emit('status', info.value)
    }
};


onMounted(() => {
    stick.value.addEventListener('mousedown', onStart, true)
    stick.value.addEventListener('touchstart', onStart, true)

    document.addEventListener('mousemove', onMove, true)
    document.addEventListener('touchmove', onMove, true)

    document.addEventListener('mouseup', onEnd, true)
    stick.value.addEventListener('touchend', onEnd, true)
})
</script>
