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
      <n-space vertical size="medium" v-if="filteredSubscriptions.length > 0">
        <n-card
          v-for="sub in filteredSubscriptions"
          :key="sub.id"
          size="small"
          hoverable
          @click="editSub(sub)"
          class="sub-card"
          :class="{ 'disabled-card': sub.is_disabled }"
        >
          <div class="sub-content">
            <div class="sub-info">
              <div class="sub-name">
                <strong>{{ sub.name }}</strong>
                <n-tag v-if="sub.is_disabled" size="small" type="error">已禁用</n-tag>
                <n-tag v-else-if="sub.notify_mode === 'global'" size="small">🌍 默认</n-tag>
                <n-tag v-else size="small" type="warning">⚙️ 自定义</n-tag>
                <n-tag v-if="sub.group_name !== 'default'" size="small" type="info" style="margin-left: 5px;">
                  {{ sub.group_name }}
                </n-tag>
              </div>
              <div class="sub-price">¥{{ sub.price }} / {{ sub.cycle_val }}{{ sub.cycle_unit === 'day' ? '天' : sub.cycle_unit === 'week' ? '周' : sub.cycle_unit === 'month' ? '月' : '年' }}</div>
              <div v-if="sub.remarks" class="sub-remarks">{{ sub.remarks }}</div>
            </div>
            <div class="sub-date">
              <div class="next-date">{{ sub.next_date }}</div>
              <div class="days-left">{{ getDaysUntil(sub.next_date) }}天后</div>
            </div>
            <div class="sub-actions" @click.stop>
              <n-space>
                <n-button 
                  size="small" 
                  @click="handleClone(sub)"
                >
                  克隆
                </n-button>
                <n-button 
                  v-if="!sub.is_disabled"
                  size="small" 
                  type="primary" 
                  @click="handleRenew(sub)"
                  :loading="renewingId === sub.id"
                >
                  进入下一周期
                </n-button>
              </n-space>
            </div>
          </div>
        </n-card>
      </n-space>
      
      <n-empty 
        v-else
        description="暂无订阅数据"
        style="margin-top: 40px;"
      >
        <template #extra>
          <n-button @click="handleAddClick" type="primary" size="small">
            添加第一个订阅
          </n-button>
        </template>
      </n-empty>
    </n-spin>
    
    <SubscriptionModal 
      v-model:show="showAddModal" 
      :subscription="editingSubscription" 
      @saved="loadData" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import axios from 'axios'
import SubscriptionModal from './SubscriptionModal.vue'

const message = useMessage()
const dialog = useDialog()

const subscriptions = ref([])
const allGroups = ref(['default'])
const loading = ref(false)
const showAddModal = ref(false)
const editingSubscription = ref(null)
const currentGroup = ref('all') // 'all' means show all groups
const renewingId = ref(null) // Track which subscription is being renewed

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

const filteredSubscriptions = computed(() => {
  if (currentGroup.value === 'all' || !currentGroup.value) {
    return subscriptions.value
  }
  return subscriptions.value.filter(sub => sub.group_name === currentGroup.value)
})

const handleAddClick = () => {
  console.log('Add button clicked')
  editingSubscription.value = null
  showAddModal.value = true
}

const handleClone = (sub) => {
  // Create a copy of the subscription without the id for cloning
  const clonedSub = { ...sub }
  delete clonedSub.id
  delete clonedSub.next_date // Reset next date to current date for new subscription
  
  // Add suffix to name to indicate it's a clone
  clonedSub.name = `${sub.name} (副本)`
  
  editingSubscription.value = clonedSub
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

const editSub = (sub) => {
  editingSubscription.value = sub
  showAddModal.value = true
}

const handleRenew = (sub) => {
  dialog.warning({
    title: '确认进入下一扣费周期',
    content: `确定要将「${sub.name}」的扣费日期更新到下一个周期吗？\n当前扣费日期：${sub.next_date}\n新扣费日期将根据订阅周期自动计算。`,
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      renewSubscription(sub.id)
    }
  })
}

const renewSubscription = async (subscriptionId) => {
  renewingId.value = subscriptionId
  try {
    const response = await axios.post(`/api/subscriptions/${subscriptionId}/renew`)
    message.success('已成功进入下一扣费周期')
    await loadData() // Refresh the subscription list
  } catch (error) {
    message.error('操作失败：' + (error.response?.data?.detail || '未知错误'))
  } finally {
    renewingId.value = null
  }
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
  gap: 12px;
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

.sub-remarks {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  padding: 2px 6px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  word-break: break-word;
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

.sub-actions {
  display: flex;
  align-items: center;
}

.disabled-card {
  opacity: 0.6;
  background-color: #f5f5f5;
}

.disabled-card .sub-name,
.disabled-card .sub-price,
.disabled-card .next-date,
.disabled-card .days-left {
  color: #999;
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
  
  .sub-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>