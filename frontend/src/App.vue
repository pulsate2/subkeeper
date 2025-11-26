<template>
  <n-config-provider :theme="darkTheme">
    <n-notification-provider>
      <n-dialog-provider>
        <n-message-provider>
          <router-view />
        </n-message-provider>
      </n-dialog-provider>
    </n-notification-provider>
  </n-config-provider>
</template>

<script setup>
import { darkTheme } from 'naive-ui'
</script>