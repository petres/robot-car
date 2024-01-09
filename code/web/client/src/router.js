import { createWebHistory, createRouter } from 'vue-router'

import Home from '@/pages/Home.vue'

// import File from '@/pages/File.vue'

const router = createRouter({
    history: createWebHistory(__webpack_public_path__),
    routes: [
        {
            name: 'home',
            component: Home, 
            // path: '/:layer?/:zoom?/:lat?/:lng?', 
            // props: route => ({
            //     layer: route.params.layer,
            //     zoom: parseInt(route.params.zoom),
            //     lng: +route.params.lng,
            //     lat: +route.params.lat,
            // })
        },
        // { path: '/file/:id', component: File, props: true, name: 'file'},   
    ]
})

export {
    router
}