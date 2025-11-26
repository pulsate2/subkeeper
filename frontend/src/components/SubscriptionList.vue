<template>
  <div class="subscription-list">
    <div class="list-header">
      <h2>订阅列表</h2>
      <n-space>
        <n-select
          v-model:value="currentGroup"
          :options="groupOptions"
          placeholder="选择分组"
          style="width: 150px;"
        />
        <n-button @click="handleAddClick" type="primary" size="small">
          + 添加订阅
        </n-button>
      </n-space>
    </div>
    
    <n-spin :show="loading">
      <n-space vertical size="medium">
        <n-card
          v-for="sub in filteredSubscriptions"
          :key="sub.id"
          size="small"
          hoverable
          @click="editSub(sub)"
          class="sub-card"
        >
          <div class="sub-content">
            <div class="sub-info">
              <div class="sub-name">
                <strong>{{ sub.name }}</strong>
                <n-tag v-if="sub.notify_mode === 'global'" size="small">🌍 默认</n-tag>
                <n-tag v-else size="small" type="warning">⚙️ 自定义</n-tag>
                <n-tag v-if="sub.group_name !== 'default'" size="small" type="info" style="margin-left: 5px;">
                  {{ sub.group_name }}
                </n-tag>
              </div>
              <div class="sub-price">¥{{ sub.price }} / {{ sub.cycle_val }}{{ sub.cycle_unit === 'day' ? '天' : sub.cycle_unit === 'week' ? '周' : sub.cycle_unit === 'month' ? '月' : '年' }}</div>
            </div>
            <div class="sub-date">
              <div class="next-date">{{ sub.next_date }}</div>
              <div class="days-left">{{ getDaysUntil(sub.next_date) }}天后</div>
            </div>
          </div>
        </n-card>
      </n-space>
    </n-spin>
    
    <n-modal v-model:show="showAddModal" preset="card" :title="editingId ? '编辑订阅' : '添加订阅'" style="width: 600px;">
      <n-form>
        <n-form-item label="分组">
          <n-select v-model:value="form.group_name" :options="allGroupOptions" placeholder="选择或输入分组名称" filterable tag />
        </n-form-item>
        <n-form-item label="服务名称">
          <n-input v-model:value="form.name" placeholder="例如: Netflix" />
        </n-form-item>
        <n-form-item label="价格">
          <n-input-number v-model:value="form.price" :min="0" style="width: 100%;" />
        </n-form-item>
        <n-form-item label="周期">
          <n-space>
            <n-input-number v-model:value="form.cycle_val" :min="1" style="width: 100px;" />
            <n-select v-model:value="form.cycle_unit" :options="cycleOptions" style="width: 100px;" />
          </n-space>
        </n-form-item>
        <n-form-item label="下次扣款日期">
          <n-date-picker v-model:formatted-value="form.next_date" type="date" format="yyyy-MM-dd" style="width: 100%;" />
        </n-form-item>
        <n-form-item label="通知设置">
          <n-switch v-model:value="useGlobal" @update:value="toggleMode">
            <template #checked>跟随默认</template>
            <template #unchecked>自定义</template>
          </n-switch>
        </n-form-item>
        <div v-if="!useGlobal">
          <n-form-item label="通知时间">
            <n-time-picker v-model:formatted-value="form.cust_time" format="HH:mm" />
          </n-form-item>
          <n-form-item label="提醒天数(逗号分隔)">
            <n-input v-model:value="form.cust_days" placeholder="例如: 7,3,1,0" />
          </n-form-item>
        </div>
        <div v-else>
          <n-alert type="info" title="将使用系统默认通知设置" />
        </div>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddModal = false">取消</n-button>
          <n-button v-if="editingId" @click="deleteSub" type="error">删除</n-button>
          <n-button @click="saveSub" type="primary">保存</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import axios from 'axios'

const message = useMessage()
const dialog = useDialog()

const subscriptions = ref([])
const allGroups = ref(['default'])
const loading = ref(false)
const showAddModal = ref(false)
const editingId = ref(null)
const useGlobal = ref(true)
const currentGroup = ref('all') // 'all' means show all groups

const form = ref({
  name: '',
  price: 0,
  cycle_val: 1,
  cycle_unit: 'month',
  next_date: null,
  notify_mode: 'global',
  cust_time: '09:00',
  cust_days: '3,1,0',
  group_name: 'default'
})

const cycleOptions = [
  { label: '天', value: 'day' },
  { label: '周', value: 'week' },
  { label: '月', value: 'month' },
  { label: '年', value: 'year' }
]

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

const filteredSubscriptions = computed(() => {
  if (currentGroup.value === 'all' || !currentGroup.value) {
    return subscriptions.value
  }
  return subscriptions.value.filter(sub => sub.group_name === currentGroup.value)
})

// Watch for changes to showAddModal to reset form when opening/closing
watch(showAddModal, (val) => {
  if (val && editingId.value) {
    // If we're showing modal for editing, the form should already be populated
  } else if (val && !editingId.value) {
    // If we're showing modal for creating, reset the form
    form.value = {
      name: '',
      price: 0,
      cycle_val: 1,
      cycle_unit: 'month',
      next_date: null,
      notify_mode: 'global',
      cust_time: '09:00',
      cust_days: '3,1,0',
      group_name: 'default'
    }
    useGlobal.value = true
  }
})

const handleAddClick = () => {
  console.log('Add button clicked')
  // Clear editing state for creating new subscription
  editingId.value = null
  form.value = {
    name: '',
    price: 0,
    cycle_val: 1,
    cycle_unit: 'month',
    next_date: null,
    notify_mode: 'global',
    cust_time: '09:00',
    cust_days: '3,1,0',
    group_name: 'default'
  }
  useGlobal.value = true
  showAddModal.value = true
}

const loadData = async () => {
  loading.value = true
  try {
    const [subscriptionsRes, groupsRes] = await Promise.all([
      axios.get('/api/subscriptions/'),
      axios.get('/api/subscriptions/groups')
    ])
    subscriptions.value = subscriptionsRes.data
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

const getDaysUntil = (dateStr) => {
  const today = new Date()
  const target = new Date(dateStr)
  const diff = Math.ceil((target - today) / (1000 * 60 * 60 * 24))
  return diff
}

const toggleMode = (value) => {
  form.value.notify_mode = value ? 'global' : 'custom'
}

const editSub = (sub) => {
  editingId.value = sub.id
  form.value = {
    name: sub.name,
    price: sub.price,
    cycle_val: sub.cycle_val,
    cycle_unit: sub.cycle_unit,
    next_date: sub.next_date,
    notify_mode: sub.notify_mode,
    cust_time: sub.cust_time || '09:00',
    cust_days: sub.cust_days || '3,1,0',
    group_name: sub.group_name || 'default'
  }
  useGlobal.value = sub.notify_mode === 'global'
  showAddModal.value = true
}

const saveSub = async () => {
  try {
    const data = {
      ...form.value,
      cust_days: useGlobal.value ? null : form.value.cust_days,
      cust_time: useGlobal.value ? null : form.value.cust_time,
      notify_mode: useGlobal.value ? 'global' : 'custom'
    }
    
    if (editingId.value) {
      await axios.put(`/api/subscriptions/${editingId.value}`, data)
      message.success('订阅已更新')
    } else {
      await axios.post('/api/subscriptions/', data)
      message.success('订阅已添加')
    }
    
    showAddModal.value = false
    editingId.value = null
    form.value = {
      name: '',
      price: 0,
      cycle_val: 1,
      cycle_unit: 'month',
      next_date: null,
      notify_mode: 'global',
      cust_time: '09:00',
      cust_days: '3,1,0',
      group_name: 'default'
    }
    useGlobal.value = true
    loadData()
  } catch (error) {
    message.error('保存失败')
  }
}

const deleteSub = () => {
  dialog.warning({
    title: '确认删除',
    content: '确定要删除这个订阅吗?',
    positiveText: '删除',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        await axios.delete(`/api/subscriptions/${editingId.value}`)
        message.success('订阅已删除')
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
.subscription-list {
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

.sub-card {
  cursor: pointer;
  transition: all 0.3s;
}

.sub-card:hover {
  transform: translateY(-2px);
}

.sub-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sub-info {
  flex: 1;
}

.sub-name {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.sub-price {
  font-size: 12px;
  color: #999;
}

.sub-date {
  text-align: right;
}

.next-date {
  font-size: 14px;
  margin-bottom: 4px;
}

.days-left {
  font-size: 12px;
  color: #18a058;
}

/* Mobile responsive styles */
@media (max-width: 768px) {
  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .sub-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .sub-date {
    text-align: left;
  }
}
</style>