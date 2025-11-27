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
          :class="{ 'disabled-card': reminder.is_disabled }"
        >
          <div class="reminder-content">
            <div class="reminder-info">
              <div class="reminder-title">
                <strong>{{ reminder.title }}</strong>
                <n-tag v-if="reminder.is_disabled" size="small" type="error">已禁用</n-tag>
                <n-tag v-else-if="reminder.is_sent" type="success" size="small">
                  已完成
                </n-tag>
                <n-tag v-if="reminder.group_name !== 'default'" size="small" type="info" style="margin-left: 5px;">
                  {{ reminder.group_name }}
                </n-tag>
              </div>
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
    
    <ReminderModal 
      v-model:show="showAddModal" 
      :reminder="editingReminder" 
      @saved="loadData" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import axios from 'axios'
import ReminderModal from './ReminderModal.vue'

const message = useMessage()
const dialog = useDialog()

const reminders = ref([])
const allGroups = ref(['default'])
const loading = ref(false)
const showAddModal = ref(false)
const editingReminder = ref(null)
const currentGroup = ref('all') // 'all' means show all groups

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
  editingReminder.value = null
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
  editingReminder.value = reminder
  showAddModal.value = true
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

.disabled-card {
  opacity: 0.6;
  background-color: #f5f5f5;
}

.disabled-card .reminder-title,
.disabled-card .reminder-content-text,
.disabled-card .reminder-time {
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