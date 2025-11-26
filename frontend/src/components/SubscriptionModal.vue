<template>
  <n-modal v-model:show="show" preset="card" :title="subscription ? '编辑订阅' : '添加订阅'" :style="modalStyle">
    <n-form ref="formRef" :model="formData" :rules="rules">
      <n-form-item label="服务名称" path="name">
        <n-input v-model:value="formData.name" placeholder="例如: Netflix" />
      </n-form-item>
      <n-form-item label="价格" path="price">
        <n-input-number v-model:value="formData.price" :min="0" :precision="2" style="width: 100%;" />
      </n-form-item>
      <n-form-item label="周期">
        <n-space>
          <n-input-number v-model:value="formData.cycle_val" :min="1" style="width: 120px;" />
          <n-select v-model:value="formData.cycle_unit" :options="cycleOptions" style="width: 100px;" />
        </n-space>
      </n-form-item>
      <n-form-item label="下次扣款日期" path="next_date">
        <n-date-picker v-model:formatted-value="formData.next_date" type="date" format="yyyy-MM-dd" style="width: 100%;" />
      </n-form-item>
      <n-form-item label="通知设置">
        <n-switch v-model:value="useGlobal">
          <template #checked>跟随默认</template>
          <template #unchecked>自定义</template>
        </n-switch>
      </n-form-item>
      <div v-if="!useGlobal">
        <n-form-item label="通知时间">
          <n-time-picker v-model:formatted-value="formData.cust_time" format="HH:mm" style="width: 100%;" />
        </n-form-item>
        <n-form-item label="提醒天数">
          <n-input v-model:value="formData.cust_days" placeholder="例如: 7,3,1,0" />
        </n-form-item>
      </div>
      <div v-else>
        <n-alert type="info" title="将使用系统默认通知设置" />
      </div>
    </n-form>
    <template #footer>
      <n-space justify="end">
        <n-button @click="show = false">取消</n-button>
        <n-button v-if="subscription" @click="deleteSub" type="error">删除</n-button>
        <n-button @click="saveSub" type="primary">保存</n-button>
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
  subscription: Object
})

const emit = defineEmits(['update:show', 'saved'])

const message = useMessage()
const dialog = useDialog()

const show = ref(props.show)
const useGlobal = ref(true)

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
  name: '',
  price: 0,
  cycle_val: 1,
  cycle_unit: 'month',
  next_date: '',
  notify_mode: 'global',
  cust_time: '09:00',
  cust_days: '3,1,0'
})

const cycleOptions = [
  { label: '月', value: 'month' },
  { label: '年', value: 'year' }
]

const rules = {
  name: { required: true, message: '请输入服务名称', trigger: 'blur' },
  price: { required: true, type: 'number', message: '请输入价格', trigger: 'blur' },
  next_date: { required: true, message: '请选择日期', trigger: 'blur' }
}

watch(() => props.show, (val) => {
  show.value = val
  if (val && props.subscription) {
    formData.value = {
      name: props.subscription.name,
      price: props.subscription.price,
      cycle_val: props.subscription.cycle_val,
      cycle_unit: props.subscription.cycle_unit,
      next_date: props.subscription.next_date,
      notify_mode: props.subscription.notify_mode,
      cust_time: props.subscription.cust_time || '09:00',
      cust_days: props.subscription.cust_days || '3,1,0'
    }
    useGlobal.value = props.subscription.notify_mode === 'global'
  } else if (val && !props.subscription) {
    formData.value = {
      name: '',
      price: 0,
      cycle_val: 1,
      cycle_unit: 'month',
      next_date: '',
      notify_mode: 'global',
      cust_time: '09:00',
      cust_days: '3,1,0'
    }
    useGlobal.value = true
  }
})

watch(show, (val) => {
  emit('update:show', val)
})

const saveSub = async () => {
  try {
    const data = {
      ...formData.value,
      notify_mode: useGlobal.value ? 'global' : 'custom',
      cust_time: useGlobal.value ? null : formData.value.cust_time,
      cust_days: useGlobal.value ? null : formData.value.cust_days
    }

    if (props.subscription) {
      await axios.put(`/api/subscriptions/${props.subscription.id}`, data)
      message.success('订阅已更新')
    } else {
      await axios.post('/api/subscriptions/', data)
      message.success('订阅已添加')
    }

    show.value = false
    emit('saved')
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
        await axios.delete(`/api/subscriptions/${props.subscription.id}`)
        message.success('订阅已删除')
        show.value = false
        emit('saved')
      } catch (error) {
        message.error('删除失败')
      }
    }
  })
}
</script>
