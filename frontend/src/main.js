import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import axios from 'axios'
import './style.css'

// Naive UI
import naive from 'naive-ui'

// Configure axios
axios.defaults.baseURL = ''

const app = createApp(App)
const pinia = createPinia()

app.use(naive)
app.use(pinia)
app.config.globalProperties.$axios = axios

app.mount('#app')