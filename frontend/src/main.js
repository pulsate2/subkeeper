import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import axios from 'axios'
import './style.css'

// Views
import LoginView from './views/LoginView.vue'
import AppContent from './AppContent.vue'

// Naive UI
import naive from 'naive-ui'

// Configure axios
axios.defaults.baseURL = ''

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: LoginView },
    { path: '/', component: AppContent }
  ]
})

const app = createApp(App)
const pinia = createPinia()

app.use(naive)
app.use(pinia)
app.use(router)
app.config.globalProperties.$axios = axios

app.mount('#app')