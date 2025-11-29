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
        <n-date-picker 
          v-model:value="formData.target_date_value" 
          type="date" 
          format="yyyy-MM-dd" 
          style="width: 100%;" 
          :clearable="false"
        />
      </n-form-item>
      <n-form-item label="提醒时间" path="target_time">
        <n-time-picker 
          v-model:value="formData.target_time_value" 
          format="HH:mm" 
          style="width: 100%;" 
          :clearable="false"
        />
      </n-form-item>
      <n-form-item label="分组" path="group_name">
        <n-select
          v-model:value="formData.group_name"
          :options="groupSelectOptions"
          placeholder="选择或输入分组"
          filterable
          tag
          :clearable="false"
          style="width: 100%;"
        />
      </n-form-item>
      <n-form-item label="通知方式">
        <n-space vertical>
          <n-checkbox v-model:checked="formData.notify_email">邮件通知</n-checkbox>
          <n-checkbox v-model:checked="formData.notify_wechat">企业微信通知</n-checkbox>
          <n-checkbox v-model:checked="formData.notify_webhook">Webhook通知</n-checkbox>
          <n-checkbox v-model:checked="formData.notify_resend">Resend邮件通知</n-checkbox>
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
const availableGroups = ref(['default'])

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
  target_date: new Date().toLocaleDateString('en-CA'),
  target_date_value: new Date().getTime(),
  target_time: '09:00',
  target_time_value: new Date().setHours(9, 0, 0, 0),
  group_name: 'default',
  notify_email: true,
  notify_wechat: true,
  notify_webhook: true,
  notify_resend: true
})

const groupSelectOptions = computed(() => {
  return availableGroups.value.map(group => ({
    label: group,
    value: group
  }))
})

const rules = {
  title: { required: true, message: '请输入提醒标题', trigger: 'blur' },
  target_date: { required: true, message: '请选择日期', trigger: 'blur' },
  target_time: { required: true, message: '请选择时间', trigger: 'blur' }
}

const loadGroups = async () => {
  try {
    const response = await axios.get('/api/reminders/groups')
    availableGroups.value = response.data.length > 0 ? ['default', ...response.data.filter(g => g !== 'default')] : ['default']
  } catch (error) {
    console.error('Failed to load groups:', error)
    availableGroups.value = ['default']
  }
}

watch(() => props.show, (val) => {
  show.value = val
  if (val) {
    loadGroups()
    
    if (props.reminder) {
      formData.value = {
        title: props.reminder.title,
        content: props.reminder.content || '',
        target_date: props.reminder.target_date,
        target_date_value: props.reminder.target_date ? new Date(props.reminder.target_date).getTime() : new Date().getTime(),
        target_time: props.reminder.target_time,
        target_time_value: props.reminder.target_time ? new Date(`2000-01-01 ${props.reminder.target_time}`) : new Date().setHours(9, 0, 0, 0),
        group_name: props.reminder.group_name || 'default',
        notify_email: props.reminder.notify_email !== undefined ? props.reminder.notify_email : true,
        notify_wechat: props.reminder.notify_wechat !== undefined ? props.reminder.notify_wechat : true,
        notify_webhook: props.reminder.notify_webhook !== undefined ? props.reminder.notify_webhook : true,
        notify_resend: props.reminder.notify_resend !== undefined ? props.reminder.notify_resend : true
      }
    } else {
      formData.value = {
        title: '',
        content: '',
        target_date: new Date().toLocaleDateString('en-CA'),
        target_date_value: new Date().getTime(),
        target_time: '09:00',
        target_time_value: new Date().setHours(9, 0, 0, 0),
        group_name: 'default',
        notify_email: true,
        notify_wechat: true,
        notify_webhook: true,
        notify_resend: true
      }
    }
  }
})

watch(show, (val) => {
  emit('update:show', val)
})

const saveReminder = async () => {
  try {
    // Convert date and time values to string format (fix timezone issue)
    if (formData.value.target_date_value) {
      const date = new Date(formData.value.target_date_value);
      // Get local date components to avoid timezone conversion issues
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      formData.value.target_date = `${year}-${month}-${day}`;
    }
    if (formData.value.target_time_value) {
      const timeDate = new Date(formData.value.target_time_value);
      const hours = timeDate.getHours().toString().padStart(2, '0');
      const minutes = timeDate.getMinutes().toString().padStart(2, '0');
      formData.value.target_time = `${hours}:${minutes}`;
    }

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