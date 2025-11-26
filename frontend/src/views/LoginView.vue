<template>
  <div class="login-container">
    <div class="login-background">
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
      </div>
    </div>
    
    <div class="login-content">
      <div class="login-header">
        <div class="logo">
          <n-icon size="48" color="#63e2b7">
            <CreditCard />
          </n-icon>
        </div>
        <h1 class="app-title">SubKeeper</h1>
        <p class="app-subtitle">订阅与提醒管理系统</p>
      </div>
      
      <n-card class="login-card" :bordered="false">
        <div class="card-header">
          <h2>欢迎回来</h2>
          <p>请输入密码以继续访问</p>
        </div>
        
        <n-form ref="formRef" :model="form" :rules="rules" size="large">
          <n-form-item path="password">
            <n-input
              v-model:value="form.password"
              type="password"
              placeholder="请输入密码"
              :maxlength="50"
              show-password-on="click"
              @keydown.enter="handleLogin"
              class="password-input"
            >
              <template #prefix>
                <n-icon :component="Lock" />
              </template>
            </n-input>
          </n-form-item>
          
          <n-form-item>
            <n-button
              type="primary"
              block
              size="large"
              :loading="loading"
              @click="handleLogin"
              class="login-button"
            >
              <template #icon>
                <n-icon v-if="!loading" :component="Login" />
              </template>
              {{ loading ? '登录中...' : '登录' }}
            </n-button>
          </n-form-item>
        </n-form>
        
        <div class="card-footer">
          <n-divider style="margin: 20px 0">
            <span class="footer-text">安全登录</span>
          </n-divider>
          <div class="security-features">
            <div class="feature">
              <n-icon size="16" color="#63e2b7">
                <Shield />
              </n-icon>
              <span>JWT 加密</span>
            </div>
            <div class="feature">
              <n-icon size="16" color="#63e2b7">
                <Clock />
              </n-icon>
              <span>30天有效期</span>
            </div>
          </div>
        </div>
      </n-card>
      
      <div class="login-footer">
        <p>© 2025 SubKeeper. 保护您的订阅管理</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { 
  CreditCard,
  Lock,
  Login,
  Shield,
  Clock
} from '@vicons/tabler'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()

const loading = ref(false)
const formRef = ref(null)

const form = reactive({
  password: ''
})

const rules = {
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: 'blur'
    },
    {
      min: 1,
      message: '密码不能为空',
      trigger: 'blur'
    }
  ]
}

const handleLogin = async () => {
  try {
    await formRef.value?.validate()
    loading.value = true
    
    const success = await authStore.login(form.password)
    
    if (success) {
      message.success('登录成功，正在跳转...')
      setTimeout(() => {
        router.push('/')
      }, 1000)
    } else {
      message.error('密码错误，请重试')
      form.password = ''
    }
  } catch (error) {
    console.error('Login error:', error)
    message.error('登录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  overflow: hidden;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 0;
}

.floating-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite ease-in-out;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
  animation-duration: 25s;
}

.shape-2 {
  width: 120px;
  height: 120px;
  top: 60%;
  right: 10%;
  animation-delay: 2s;
  animation-duration: 30s;
}

.shape-3 {
  width: 60px;
  height: 60px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
  animation-duration: 20s;
}

.shape-4 {
  width: 100px;
  height: 100px;
  top: 10%;
  right: 30%;
  animation-delay: 1s;
  animation-duration: 35s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.7;
  }
  25% {
    transform: translateY(-20px) rotate(90deg);
    opacity: 0.9;
  }
  50% {
    transform: translateY(10px) rotate(180deg);
    opacity: 0.5;
  }
  75% {
    transform: translateY(-15px) rotate(270deg);
    opacity: 0.8;
  }
}

.login-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  padding: 20px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  margin-bottom: 16px;
  display: inline-block;
  padding: 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  backdrop-filter: blur(10px);
}

.app-title {
  font-size: 32px;
  font-weight: 700;
  color: white;
  margin: 0 0 8px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.app-subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-weight: 400;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.05);
  overflow: hidden;
}

.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.card-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.card-header p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.password-input {
  margin-bottom: 8px;
}

.password-input :deep(.n-input__input-el) {
  background-color: rgba(255, 255, 255, 0.9) !important;
  color: #1a1a1a !important;
  border: 1px solid rgba(0, 0, 0, 0.1) !important;
}

.password-input :deep(.n-input__border) {
  border-color: rgba(0, 0, 0, 0.2) !important;
}

.password-input :deep(.n-input__state-border) {
  border-color: rgba(0, 0, 0, 0.2) !important;
}

.password-input :deep(.n-input__placeholder) {
  color: #999 !important;
}

.login-button {
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.card-footer {
  margin-top: 24px;
}

.footer-text {
  font-size: 12px;
  color: #999;
}

.security-features {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 16px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #666;
}

.login-footer {
  text-align: center;
  margin-top: 32px;
}

.login-footer p {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-content {
    padding: 16px;
  }
  
  .app-title {
    font-size: 28px;
  }
  
  .login-card {
    margin: 0 16px;
  }
  
  .security-features {
    gap: 16px;
  }
}

/* 暗色主题适配 */
@media (prefers-color-scheme: dark) {
  .login-card {
    background: rgba(24, 24, 28, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .card-header h2 {
    color: white;
  }
  
  .card-header p {
    color: rgba(255, 255, 255, 0.7);
  }
  
  .footer-text {
    color: rgba(255, 255, 255, 0.5);
  }
  
  .feature {
    color: rgba(255, 255, 255, 0.7);
  }
  
  .password-input :deep(.n-input__input-el) {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
  }
  
  .password-input :deep(.n-input__border) {
    border-color: rgba(255, 255, 255, 0.3) !important;
  }
  
  .password-input :deep(.n-input__state-border) {
    border-color: rgba(255, 255, 255, 0.3) !important;
  }
  
  .password-input :deep(.n-input__placeholder) {
    color: rgba(255, 255, 255, 0.6) !important;
  }
}
</style>