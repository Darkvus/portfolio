import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import 'virtual:uno.css'
import App from './App.vue'
import Home from './pages/Home.vue'
import Blog from './pages/Blog.vue'
import BlogPost from './pages/BlogPost.vue'
import About from './pages/About.vue'
import Admin from './pages/Admin.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/blog', component: Blog },
    { path: '/blog/:slug', component: BlogPost },
    { path: '/about', component: About },
    { path: '/admin', component: Admin },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

createApp(App).use(router).mount('#app')
