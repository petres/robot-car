import { createWebHistory, createRouter } from 'vue-router'

import Detail from '@/pages/Detail.vue'
import Full from '@/pages/Full.vue'

// import File from '@/pages/File.vue'

const router = createRouter({
    history: createWebHistory(__webpack_public_path__),
    routes: [
        {
            name: 'detail',
            component: Detail, 
            // path: '/:layer?/:zoom?/:lat?/:lng?', 
            // props: route => ({
            //     layer: route.params.layer,
            //     zoom: parseInt(route.params.zoom),
            //     lng: +route.params.lng,
            //     lat: +route.params.lat,
            // })
        },
        {
            name: 'detail',
            component: Detail,
        },
        {
            name: 'full',
            component: Full,
        },
        // { path: '/file/:id', component: File, props: true, name: 'file'},   
    ]
})

export {
    router
}