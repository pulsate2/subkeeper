<template>
  <n-modal v-model:show="show" preset="card" :title="reminder ? '编辑提醒' : '添加提醒'" :style="modalStyle">
    <n-form ref="formRef" :model="formData" :rules="rules">
      <n-form-item label="提醒标题" path="title">
        <n-input v-model:value="formData.title" placeholder="例如: 会议提醒" />
      </n-form-item>
      <n-form-item label="提醒内容" path="content">
        <n-input type="textarea" v-model:value="formData.content" placeholder="详细描述提醒内容" :rows="3" />
      </n-form-item>
      <n-form-item label="提醒日期" path="target_date">
        <n-date-picker v-model:formatted-value="formData.target_date" type="date" format="yyyy-MM-dd" style="width: 100%;" />
      </n-form-item>
      <n-form-item label="提醒时间" path="target_time">
        <n-time-picker v-model:formatted-value="formData.target_time" format="HH:mm" style="width: 100%;" />
      </n-form-item>
      <n-form-item label="通知方式">
        <n-space vertical>
          <n-checkbox v-model:checked="formData.notify_email">邮件通知</n-checkbox>
          <n-checkbox v-model:checked="formData.notify_wechat">企业微信通知</n-checkbox>
          <n-checkbox v-model:checked="formData.notify_webhook">Webhook通知</n-checkbox>
        </n-space>
      </n-form-item>
    </n-form>
    <template #footer>
      <n-space justify="end">
        <n-button @click="show = false">取消</n-button>
        <n-button v-if="reminder" @click="deleteReminder" type="error">删除</n-button>
        <n-button @click="saveReminder" type="primary">保存</n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import axios from 'axios'

const props = defineProps({
  show: Boolean,
  reminder: Object
})

const emit = defineEmits(['update:show', 'saved'])

const message = useMessage()
const dialog = useDialog()

const show = ref(props.show)

// Reactive screen size detection
const isMobile = ref(window.innerWidth < 768)

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

const formData = ref({
  title: '',
  content: '',
  target_date: new Date().toISOString().split('T')[0],
  target_time: '09:00',
  notify_email: true,
  notify_wechat: true,
  notify_webhook: true
})

const rules = {
  title: { required: true, message: '请输入提醒标题', trigger: 'blur' },
  target_date: { required: true, message: '请选择日期', trigger: 'blur' },
  target_time: { required: true, message: '请选择时间', trigger: 'blur' }
}

watch(() => props.show, (val) => {
  show.value = val
  if (val && props.reminder) {
    formData.value = {
      title: props.reminder.title,
      content: props.reminder.content || '',
      target_date: props.reminder.target_date,
      target_time: props.reminder.target_time,
      notify_email: props.reminder.notify_email !== undefined ? props.reminder.notify_email : true,
      notify_wechat: props.reminder.notify_wechat !== undefined ? props.reminder.notify_wechat : true,
      notify_webhook: props.reminder.notify_webhook !== undefined ? props.reminder.notify_webhook : true
    }
  } else if (val && !props.reminder) {
    formData.value = {
      title: '',
      content: '',
      target_date: new Date().toISOString().split('T')[0],
      target_time: '09:00',
      notify_email: true,
      notify_wechat: true,
      notify_webhook: true
    }
  }
})

watch(show, (val) => {
  emit('update:show', val)
})

const saveReminder = async () => {
  try {
    const data = { ...formData.value }

    if (props.reminder) {
      await axios.put(`/api/reminders/${props.reminder.id}`, data)
      message.success('提醒已更新')
    } else {
      await axios.post('/api/reminders/', data)
      message.success('提醒已添加')
    }

    show.value = false
    emit('saved')
  } catch (error) {
    message.error('保存失败')
  }
}

const deleteReminder = () => {
  dialog.warning({
    title: '确认删除',
    content: '确定要删除这个提醒吗?',
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await axios.delete(`/api/reminders/${props.reminder.id}`)
        message.success('提醒已删除')
        show.value = false
        emit('saved')
      } catch (error) {
        message.error('删除失败')
      }
    }
  })
}
</script>