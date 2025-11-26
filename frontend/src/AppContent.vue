<template>
  <div class="app-container">
    <div class="header">
      <h1>📋 SubKeeper</h1>
      <n-space>
        <n-button @click="testAPI" size="small" tertiary>测试 API</n-button>
        <n-button @click="showSettings = true" size="small" type="primary">⚙️ 设置</n-button>
      </n-space>
    </div>
    
    <div class="main-content">
      <n-grid 
        :cols="isMobile ? 1 : 2" 
        :x-gap="16" 
        :y-gap="16"
        :responsive="'screen'"
      >
        <n-gi>
          <SubscriptionList />
        </n-gi>
        <n-gi>
          <ReminderList />
        </n-gi>
      </n-grid>
    </div>
    
    <SettingsModal v-model:show="showSettings" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMessage } from 'naive-ui'
import axios from 'axios'
import SubscriptionList from './components/SubscriptionList.vue'
import ReminderList from './components/ReminderList.vue'
import SettingsModal from './components/SettingsModal.vue'

const showSettings = ref(false)
const message = useMessage()

// Reactive mobile detection
const isMobile = ref(window.innerWidth < 768)

const updateMobileStatus = () => {
  isMobile.value = window.innerWidth < 768
}

// Add event listener for window resize
if (typeof window !== 'undefined') {
  window.addEventListener('resize', updateMobileStatus)
}

const testAPI = async () => {
  try {
    const response = await axios.get('/api/health')
    message.success('✅ 后端连接成功: ' + JSON.stringify(response.data))
  } catch (error) {
    message.error('❌ 后端连接失败: ' + error.message)
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-container {
  width: 100%;
  min-height: 100vh;
  background: #18181c;
  color: #fff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.header {
  border-bottom: 1px solid #2c2c2c;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #1f1f23;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
}

.btn {
  padding: 8px 16px;
  background: #63e2b7;
  border: none;
  border-radius: 6px;
  color: #000;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn:hover {
  background: #4ecca3;
  transform: translateY(-1px);
}

.main-content {
  padding: 40px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Mobile responsive styles */
@media (max-width: 768px) {
  .header {
    padding: 15px 16px;
  }
  
  .header h1 {
    font-size: 20px;
  }
  
  .main-content {
    padding: 20px 16px;
  }
  
  .n-grid {
    gap: 12px !important;
  }
}

.welcome {
  text-align: center;
  padding: 60px 20px;
}

.welcome h2 {
  font-size: 32px;
  margin-bottom: 16px;
}

.welcome p {
  font-size: 18px;
  color: #999;
  margin-bottom: 40px;
}

.status {
  background: #1f1f23;
  border: 1px solid #2c2c2c;
  border-radius: 8px;
  padding: 24px;
  max-width: 500px;
  margin: 0 auto;
}

.status p {
  margin: 12px 0;
  font-size: 16px;
  color: #63e2b7;
}
</style>