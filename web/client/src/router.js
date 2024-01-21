import { createWebHistory, createRouter } from 'vue-router'

import Detail from '@/pages/Detail.vue'
import Full from '@/pages/Full.vue'

// import File from '@/pages/File.vue'

const router = createRouter({
    history: createWebHistory(__webpack_public_path__),
    routes: [
        {
            name: 'detail',
            path: '/detail',
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