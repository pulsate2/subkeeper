<template>
  <n-modal v-model:show="show" preset="card" title="系统设置" :style="modalStyle">
    <n-tabs type="line">
      <n-tab-pane name="notification" tab="通知配置">
        <n-form>
          <!-- SMTP 邮箱配置 -->
          <n-form-item label="SMTP 邮箱配置">
            <n-collapse>
              <n-collapse-item title="SMTP 邮箱设置" name="smtp">
                <n-form-item label="SMTP 服务器">
                  <n-input 
                    v-model:value="smtpConfig.host" 
                    placeholder="smtp.example.com" 
                  />
                </n-form-item>
                <n-form-item label="SMTP 端口">
                  <n-input-number 
                    v-model:value="smtpConfig.port" 
                    :min="1" 
                    :max="65535"
                    placeholder="587" 
                    style="width: 100%"
                  />
                </n-form-item>
                <n-form-item label="用户名">
                  <n-input 
                    v-model:value="smtpConfig.username" 
                    placeholder="user@example.com" 
                  />
                </n-form-item>
                <n-form-item label="密码">
                  <n-input 
                    v-model:value="smtpConfig.password" 
                    type="password"
                    placeholder="密码" 
                  />
                </n-form-item>
                <n-form-item label="发送邮箱">
                  <n-input 
                    v-model:value="smtpConfig.from" 
                    placeholder="from@example.com" 
                  />
                </n-form-item>
                <n-form-item label="接收邮箱">
                  <n-input 
                    v-model:value="smtpConfig.to" 
                    placeholder="to@example.com" 
                  />
                </n-form-item>
                <n-form-item label="启用 TLS">
                  <n-switch v-model:value="smtpConfig.use_tls" />
                </n-form-item>
              </n-collapse-item>
            </n-collapse>
          </n-form-item>

          <!-- 企业微信配置 -->
          <n-form-item label="企业微信配置">
            <n-collapse>
              <n-collapse-item title="企业微信设置" name="wechat">
                <n-form-item label="企业 ID (corpid)">
                  <n-input 
                    v-model:value="wechatConfig.corpid" 
                    placeholder="企业ID" 
                  />
                </n-form-item>
                <n-form-item label="应用 Secret">
                  <n-input 
                    v-model:value="wechatConfig.secret" 
                    placeholder="应用Secret" 
                  />
                </n-form-item>
                <n-form-item label="应用 AgentId">
                  <n-input-number 
                    v-model:value="wechatConfig.agentid" 
                    placeholder="AgentId" 
                    style="width: 100%"
                  />
                </n-form-item>
                <n-form-item label="接收人">
                  <n-input 
                    v-model:value="wechatConfig.touser" 
                    placeholder="@all 或指定用户" 
                  />
                </n-form-item>
              </n-collapse-item>
            </n-collapse>
          </n-form-item>

          <!-- 企业微信 Webhook 配置 -->
          <n-form-item label="企业微信 Webhook 配置">
            <n-collapse>
              <n-collapse-item title="企业微信 Webhook 设置" name="webhook">
                <n-form-item label="Webhook Key">
                  <n-input 
                    v-model:value="webhookConfig.webhook_key" 
                    placeholder="Webhook Key" 
                  />
                </n-form-item>
              </n-collapse-item>
            </n-collapse>
          </n-form-item>

          <!-- Resend 配置 -->
          <n-form-item label="Resend 邮件配置">
            <n-collapse>
              <n-collapse-item title="Resend 设置" name="resend">
                <n-form-item label="API Key">
                  <n-input 
                    v-model:value="resendConfig.api_key" 
                    placeholder="re_xxxxxxxxxxxx" 
                  />
                </n-form-item>
                <n-form-item label="发送邮箱">
                  <n-input 
                    v-model:value="resendConfig.from" 
                    placeholder="onboarding@resend.dev" 
                  />
                </n-form-item>
                <n-form-item label="接收邮箱">
                  <n-input 
                    v-model:value="resendConfig.to" 
                    placeholder="user@example.com" 
                  />
                </n-form-item>
              </n-collapse-item>
            </n-collapse>
          </n-form-item>
        </n-form>
      </n-tab-pane>
      <n-tab-pane name="defaults" tab="默认策略">
        <n-form>
          <n-form-item label="默认通知时间">
            <n-time-picker 
              v-model:value="formData.global_time_value" 
              format="HH:mm" 
              style="width: 100%;" 
              :clearable="false"
            />
          </n-form-item>
          <n-form-item label="默认提醒天数">
            <n-input v-model:value="formData.global_days" placeholder="例如: 3,1,0" />
          </n-form-item>
        </n-form>
      </n-tab-pane>
      <n-tab-pane name="backup" tab="数据备份">
        <n-space vertical>
          <n-button @click="exportData" type="primary">导出数据</n-button>
          <n-upload 
            @change="importData" 
            :show-file-list="false"
            accept=".json"
          >
            <n-button>导入数据</n-button>
          </n-upload>
          <n-alert type="warning" title="注意: 导入数据会清空当前所有数据" />
        </n-space>
      </n-tab-pane>
    </n-tabs>
    <template #footer>
      <n-space justify="end">
        <n-button @click="show = false">取消</n-button>
        <n-button @click="saveSettings" type="primary">保存</n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useMessage } from 'naive-ui'
import axios from 'axios'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['update:show'])

const message = useMessage()
const show = ref(props.show)

const smtpConfig = ref({
  host: '',
  port: 587,
  username: '',
  password: '',
  from: '',
  to: '',
  use_tls: true
})

const wechatConfig = ref({
  corpid: '',
  secret: '',
  agentid: null,
  touser: '@all'
})

const webhookConfig = ref({
  webhook_key: ''
})

const resendConfig = ref({
  api_key: '',
  from: '',
  to: ''
})

const formData = ref({
  global_time: '09:00',
  global_time_value: new Date().setHours(9, 0, 0, 0),
  global_days: '3,1,0'
})

watch(() => props.show, async (val) => {
  show.value = val
  if (val) {
    await loadSettings()
  }
})

watch(show, (val) => {
  emit('update:show', val)
})

// Reactive screen size detection
const isMobile = ref(typeof window !== 'undefined' && window.innerWidth < 768)

const updateScreenSize = () => {
  isMobile.value = window.innerWidth < 768
}

// Add event listener for window resize
if (typeof window !== 'undefined') {
  window.addEventListener('resize', updateScreenSize)
}

// Responsive modal style based on screen size
const modalStyle = computed(() => {
  return {
    width: isMobile.value ? '90%' : '600px',
    maxWidth: '90%',
    margin: isMobile.value ? '16px auto' : 'auto'
  }
})

const loadSettings = async () => {
  try {
    const res = await axios.get('/api/settings/')
    const settings = res.data
    
    // Load SMTP config
    if (settings.smtp_conf) {
      smtpConfig.value = {
        ...smtpConfig.value,
        ...settings.smtp_conf
      }
    }
    
    // Load WeChat config
    if (settings.wechat_conf) {
      wechatConfig.value = {
        ...wechatConfig.value,
        ...settings.wechat_conf
      }
    }
    
    // Load Webhook config
    if (settings.webhook_conf) {
      webhookConfig.value = {
        ...webhookConfig.value,
        ...settings.webhook_conf
      }
    }
    
    // Load Resend config
    if (settings.resend_conf) {
      resendConfig.value = {
        ...resendConfig.value,
        ...settings.resend_conf
      }
    }
    
    // Load global settings
    const globalTime = settings.global_time || '09:00';
    formData.value = {
      global_time: globalTime,
      global_time_value: new Date(`2000-01-01 ${globalTime}`),
      global_days: settings.global_days ? settings.global_days.join(',') : '3,1,0'
    }
  } catch (error) {
    message.error('加载设置失败')
  }
}

const saveSettings = async () => {
  try {
    // Convert time value to string format
    if (formData.value.global_time_value) {
      const timeDate = new Date(formData.value.global_time_value);
      const hours = timeDate.getHours().toString().padStart(2, '0');
      const minutes = timeDate.getMinutes().toString().padStart(2, '0');
      formData.value.global_time = `${hours}:${minutes}`;
    }

    const data = {
      smtp_conf: smtpConfig.value.host ? smtpConfig.value : null,
      wechat_conf: wechatConfig.value.corpid ? wechatConfig.value : null,
      webhook_conf: webhookConfig.value.webhook_key ? webhookConfig.value : null,
      resend_conf: resendConfig.value.api_key ? resendConfig.value : null,
      global_time: formData.value.global_time,
      global_days: formData.value.global_days.split(',').map(d => parseInt(d.trim()))
    }
    
    await axios.put('/api/settings/', data)
    message.success('设置已保存')
    show.value = false
  } catch (error) {
    message.error('保存设置失败')
  }
}

const exportData = async () => {
  try {
    const response = await axios.get('/api/export', { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `subkeeper_backup_${new Date().toISOString().slice(0,10)}.json`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    message.success('数据已导出')
  } catch (error) {
    message.error('导出失败')
  }
}

const importData = async ({ file }) => {
  try {
    const formData = new FormData()
    formData.append('file', file.file)
    
    await axios.post('/api/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    message.success('数据已导入')
    show.value = false
  } catch (error) {
    message.error('导入失败')
  }
}
</script>