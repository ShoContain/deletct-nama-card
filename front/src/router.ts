import { createRouter,createWebHistory } from "vue-router"
import Home from "./pages/Home.vue"
import Example from "./pages/Example.vue"

const routes = [
    { name: "home", path: "/", component: Home },
    { name: "example", path: "/example", component: Example },
]

// ルーターの作成
export const router = createRouter({
    history: createWebHistory(),
    routes,
})
