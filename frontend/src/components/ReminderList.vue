<template>
  <div class="reminder-list">
    <div class="list-header">
      <h2>待办提醒</h2>
      <n-space>
        <n-select
          v-model:value="currentGroup"
          :options="groupOptions"
          placeholder="选择分组"
          style="width: 150px;"
        />
        <n-button @click="handleAddClick" type="primary" size="small">
          + 添加提醒
        </n-button>
      </n-space>
    </div>
    
    <n-spin :show="loading">
      <n-space vertical size="medium">
        <n-card
          v-for="reminder in filteredReminders"
          :key="reminder.id"
          size="small"
          hoverable
          @click="editReminder(reminder)"
          class="reminder-card"
        >
          <div class="reminder-content">
            <div class="reminder-info">
              <div class="reminder-title">
                <strong>{{ reminder.title }}</strong>
                <n-tag v-if="reminder.group_name !== 'default'" size="small" type="info" style="margin-left: 5px;">
                  {{ reminder.group_name }}
                </n-tag>
              </div>
              <n-tag v-if="reminder.is_sent" type="success" size="small">
                已完成
              </n-tag>
            </div>
            <div v-if="reminder.content" class="reminder-content-text">
              {{ reminder.content }}
            </div>
            <div class="reminder-time">
              {{ reminder.target_date }} {{ reminder.target_time }}
            </div>
          </div>
        </n-card>
        
        <n-empty v-if="!loading && filteredReminders.length === 0" description="暂无提醒" />
      </n-space>
    </n-spin>
    
    <n-modal v-model:show="showAddModal" preset="card" :title="editingId ? '编辑提醒' : '添加提醒'" style="width: 500px;">
      <n-form>
        <n-form-item label="分组">
          <n-select v-model:value="form.group_name" :options="allGroupOptions" placeholder="选择或输入分组名称" filterable tag />
        </n-form-item>
        <n-form-item label="标题">
          <n-input v-model:value="form.title" placeholder="提醒事项" />
        </n-form-item>
        <n-form-item label="内容">
          <n-input v-model:value="form.content" type="textarea" placeholder="提醒内容" />
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
import { ref, onMounted, computed } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import axios from 'axios'

const message = useMessage()
const dialog = useDialog()

const reminders = ref([])
const allGroups = ref(['default'])
const loading = ref(false)
const showAddModal = ref(false)
const editingId = ref(null)
const currentGroup = ref('all') // 'all' means show all groups

const form = ref({
  title: '',
  content: '',
  target_date: null,
  target_time: '09:00',
  group_name: 'default'
})

// Computed properties
const groupOptions = computed(() => {
  const options = [{ label: '全部', value: 'all' }]
  allGroups.value.forEach(group => {
    options.push({ label: group, value: group })
  })
  return options
})

const allGroupOptions = computed(() => {
  return allGroups.value.map(group => ({ label: group, value: group }))
})

const filteredReminders = computed(() => {
  if (currentGroup.value === 'all' || !currentGroup.value) {
    return reminders.value
  }
  return reminders.value.filter(reminder => reminder.group_name === currentGroup.value)
})

const handleAddClick = () => {
  console.log('Add reminder button clicked')
  showAddModal.value = true
}

const loadData = async () => {
  loading.value = true
  try {
    const [remindersRes, groupsRes] = await Promise.all([
      axios.get('/api/reminders/'),
      axios.get('/api/reminders/groups')
    ])
    reminders.value = remindersRes.data
    allGroups.value = groupsRes.data.length > 0 ? groupsRes.data : ['default']
    
    // Ensure 'default' group is always available
    if (!allGroups.value.includes('default')) {
      allGroups.value.unshift('default')
    }
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
    content: reminder.content || '',
    target_date: reminder.target_date,
    target_time: reminder.target_time,
    group_name: reminder.group_name || 'default'
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
    form.value = { title: '', content: '', target_date: null, target_time: '09:00', group_name: 'default' }
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
  flex-direction: column;
  gap: 4px;
}

.reminder-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.reminder-content-text {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.reminder-time {
  font-size: 14px;
  color: #999;
}

/* Mobile responsive styles */
@media (max-width: 768px) {
  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .reminder-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .reminder-time {
    font-size: 12px;
  }
}
</style>