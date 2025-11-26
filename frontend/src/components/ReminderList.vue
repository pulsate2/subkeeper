<template>
  <div class="reminder-list">
    <div class="list-header">
      <h2>待办提醒</h2>
      <n-button @click="handleAddClick" type="primary" size="small">
        + 添加提醒
      </n-button>
    </div>
    
    <n-spin :show="loading">
      <n-space vertical size="medium">
        <n-card
          v-for="reminder in reminders"
          :key="reminder.id"
          size="small"
          hoverable
          @click="editReminder(reminder)"
          class="reminder-card"
        >
          <div class="reminder-content">
            <div class="reminder-info">
              <strong>{{ reminder.title }}</strong>
              <n-tag v-if="reminder.is_sent" type="success" size="small" style="margin-left: 8px;">
                已完成
              </n-tag>
            </div>
            <div class="reminder-time">
              {{ reminder.target_date }} {{ reminder.target_time }}
            </div>
          </div>
        </n-card>
        
        <n-empty v-if="!loading && reminders.length === 0" description="暂无提醒" />
      </n-space>
    </n-spin>
    
    <n-modal v-model:show="showAddModal" preset="card" :title="editingId ? '编辑提醒' : '添加提醒'" style="width: 500px;">
      <n-form>
        <n-form-item label="标题">
          <n-input v-model:value="form.title" placeholder="提醒事项" />
        </n-form-item>
        <n-form-item label="日期">
          <n-date-picker v-model:formatted-value="form.target_date" type="date" format="yyyy-MM-dd" style="width: 100%;" />
        </n-form-item>
        <n-form-item label="时间">
          <n-time-picker v-model:formatted-value="form.target_time" format="HH:mm" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddModal = false">取消</n-button>
          <n-button v-if="editingId" @click="deleteReminder" type="error">删除</n-button>
          <n-button @click="saveReminder" type="primary">保存</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import axios from 'axios'

const message = useMessage()
const dialog = useDialog()

const reminders = ref([])
const loading = ref(false)
const showAddModal = ref(false)
const editingId = ref(null)

const form = ref({
  title: '',
  target_date: null,
  target_time: '09:00'
})

const handleAddClick = () => {
  console.log('Add reminder button clicked')
  showAddModal.value = true
}

const loadData = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/reminders/')
    reminders.value = res.data
  } catch (error) {
    message.error('加载失败')
  } finally {
    loading.value = false
  }
}

const editReminder = (reminder) => {
  editingId.value = reminder.id
  form.value = {
    title: reminder.title,
    target_date: reminder.target_date,
    target_time: reminder.target_time
  }
  showAddModal.value = true
}

const saveReminder = async () => {
  try {
    if (editingId.value) {
      await axios.put(`/api/reminders/${editingId.value}`, form.value)
      message.success('提醒已更新')
    } else {
      await axios.post('/api/reminders/', form.value)
      message.success('提醒已添加')
    }
    
    showAddModal.value = false
    editingId.value = null
    form.value = { title: '', target_date: null, target_time: '09:00' }
    loadData()
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
        await axios.delete(`/api/reminders/${editingId.value}`)
        message.success('提醒已删除')
        showAddModal.value = false
        editingId.value = null
        loadData()
      } catch (error) {
        message.error('删除失败')
      }
    }
  })
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.reminder-list {
  padding: 16px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.list-header h2 {
  margin: 0;
  color: #fff;
}

.reminder-card {
  cursor: pointer;
  transition: all 0.3s;
}

.reminder-card:hover {
  transform: translateY(-2px);
}

.reminder-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reminder-info {
  display: flex;
  align-items: center;
}

.reminder-time {
  font-size: 14px;
  color: #999;
}
</style>