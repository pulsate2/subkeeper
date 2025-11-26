<template>
  <n-modal v-model:show="show" preset="card" title="系统设置" style="width: 600px;">
    <n-tabs type="line">
      <n-tab-pane name="notification" tab="通知配置">
        <n-form>
          <n-form-item label="SMTP 邮箱配置">
            <n-input 
              v-model:value="formData.smtp_conf" 
              type="textarea" 
              :rows="6"
              placeholder='{"host":"smtp.example.com","port":587,"username":"user","password":"pass","from":"from@example.com","to":"to@example.com","use_tls":true}' 
            />
          </n-form-item>
          <n-form-item label="企业微信配置">
            <n-input 
              v-model:value="formData.wechat_conf" 
              type="textarea" 
              :rows="5"
              placeholder='{"corpid":"xxxxx","secret":"xxxxx","agentid":1000001,"touser":"@all"}' 
            />
          </n-form-item>
          <n-form-item label="企业微信 Webhook 配置">
            <n-input 
              v-model:value="formData.webhook_conf" 
              type="textarea" 
              :rows="3"
              placeholder='{"webhook_key":"your-webhook-key"}' 
            />
          </n-form-item>
        </n-form>
      </n-tab-pane>
      <n-tab-pane name="defaults" tab="默认策略">
        <n-form>
          <n-form-item label="默认通知时间">
            <n-time-picker v-model:formatted-value="formData.global_time" format="HH:mm" style="width: 100%;" />
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
import { ref, watch } from 'vue'
import { useMessage } from 'naive-ui'
import axios from 'axios'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['update:show'])

const message = useMessage()
const show = ref(props.show)

const formData = ref({
  smtp_conf: '',
  wechat_conf: '',
  webhook_conf: '',
  global_time: '09:00',
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

const loadSettings = async () => {
  try {
    const res = await axios.get('/api/settings/')
    const settings = res.data
    
    formData.value = {
      smtp_conf: settings.smtp_conf ? JSON.stringify(settings.smtp_conf, null, 2) : '',
      wechat_conf: settings.wechat_conf ? JSON.stringify(settings.wechat_conf, null, 2) : '',
      webhook_conf: settings.webhook_conf ? JSON.stringify(settings.webhook_conf, null, 2) : '',
      global_time: settings.global_time || '09:00',
      global_days: settings.global_days ? settings.global_days.join(',') : '3,1,0'
    }
  } catch (error) {
    message.error('加载设置失败')
  }
}

const saveSettings = async () => {
  try {
    const data = {
      smtp_conf: formData.value.smtp_conf ? JSON.parse(formData.value.smtp_conf) : null,
      wechat_conf: formData.value.wechat_conf ? JSON.parse(formData.value.wechat_conf) : null,
      webhook_conf: formData.value.webhook_conf ? JSON.parse(formData.value.webhook_conf) : null,
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