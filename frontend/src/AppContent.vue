<template>
  <div class="app-container">
    <n-layout has-sider>
      <n-layout-sider
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="240"
        :collapsed="collapsed"
        show-trigger
        @collapse="collapsed = true"
        @expand="collapsed = false"
      >
        <n-menu
          :collapsed="collapsed"
          :collapsed-width="64"
          :collapsed-icon-size="22"
          :options="menuOptions"
          :value="activeKey"
          @update:value="handleMenuSelect"
        />
      </n-layout-sider>
      
      <n-layout>
        <n-layout-header bordered class="header">
          <div class="header-content">
            <h1>SubKeeper</h1>
            <n-space>
              <n-button @click="showSettings = true">
                <template #icon>
                  <n-icon><Settings /></n-icon>
                </template>
                设置
              </n-button>
              <n-button @click="handleLogout">
                <template #icon>
                  <n-icon><Logout /></n-icon>
                </template>
                退出
              </n-button>
            </n-space>
          </div>
        </n-layout-header>
        
        <n-layout-content class="main-content">
          <div v-if="activeKey === 'subscriptions'">
            <SubscriptionList />
          </div>
          <div v-else-if="activeKey === 'reminders'">
            <ReminderList />
          </div>
          <div v-else class="welcome">
            <h2>欢迎使用 SubKeeper</h2>
            <p>订阅和提醒管理系统</p>
            <div class="status">
              <p>✅ 系统运行正常</p>
              <p>📱 支持邮件和微信通知</p>
              <p>🔔 智能提醒功能</p>
            </div>
          </div>
        </n-layout-content>
      </n-layout>
    </n-layout>

    <!-- Settings Modal -->
    <SettingsModal v-model:show="showSettings" />
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { 
  Settings,
  Logout,
  CreditCard,
  Bell,
  Home
} from '@vicons/tabler'
import { useAuthStore } from './stores/auth'
import SubscriptionList from './components/SubscriptionList.vue'
import ReminderList from './components/ReminderList.vue'
import SettingsModal from './components/SettingsModal.vue'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()

const collapsed = ref(false)
const activeKey = ref('home')
const showSettings = ref(false)

const menuOptions = [
  {
    label: '首页',
    key: 'home',
    icon: () => h(Home)
  },
  {
    label: '订阅管理',
    key: 'subscriptions',
    icon: () => h(CreditCard)
  },
  {
    label: '提醒管理',
    key: 'reminders',
    icon: () => h(Bell)
  }
]

const handleMenuSelect = (key) => {
  activeKey.value = key
}

const handleLogout = () => {
  authStore.logout()
  message.success('已退出登录')
  router.push('/login')
}

onMounted(async () => {
  // Verify token on app load
  if (authStore.isAuthenticated) {
    const isValid = await authStore.verifyToken()
    if (!isValid) {
      message.warning('登录已过期，请重新登录')
      router.push('/login')
    }
  } else {
    router.push('/login')
  }
})
</script>

<style scoped>
.app-container {
  width: 100%;
  min-height: 100vh;
  background: #18181c;
  color: #fff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.header {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #1f1f23;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.main-content {
  padding: 24px;
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