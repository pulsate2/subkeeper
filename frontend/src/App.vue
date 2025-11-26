<template>
  <n-config-provider :theme="darkTheme">
    <n-notification-provider>
      <n-dialog-provider>
        <n-message-provider>
          <AppContent />
        </n-message-provider>
      </n-dialog-provider>
    </n-notification-provider>
  </n-config-provider>
</template>

<script setup>
import { darkTheme } from 'naive-ui'
import AppContent from './AppContent.vue'
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