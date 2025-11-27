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
        <n-date-picker 
          v-model:value="formData.next_date_value" 
          type="date" 
          format="yyyy-MM-dd" 
          style="width: 100%;" 
          :clearable="false"
        />
      </n-form-item>
      <n-form-item label="通知设置">
        <n-space vertical>
          <n-form-item label="通知方式">
            <n-space vertical>
              <n-checkbox v-model:checked="formData.notify_email">邮件通知</n-checkbox>
              <n-checkbox v-model:checked="formData.notify_wechat">企业微信通知</n-checkbox>
              <n-checkbox v-model:checked="formData.notify_webhook">Webhook通知</n-checkbox>
            </n-space>
          </n-form-item>
          <n-form-item label="通知时间设置">
            <n-switch v-model:value="useGlobal">
              <template #checked>跟随默认</template>
              <template #unchecked>自定义</template>
            </n-switch>
            <div v-if="!useGlobal" style="margin-top: 10px;">
              <n-form-item label="通知时间">
                <n-time-picker 
                  v-model:formatted-value="formData.cust_time" 
                  format="HH:mm" 
                  value-format="HH:mm"
                  style="width: 100%;" 
                  :clearable="false"
                />
              </n-form-item>
              <n-form-item label="提醒天数">
                <n-input v-model:value="formData.cust_days" placeholder="例如: 7,3,1,0" />
              </n-form-item>
            </div>
            <div v-else style="margin-top: 10px;">
              <n-alert type="info" title="将使用系统默认通知时间和天数" />
            </div>
          </n-form-item>
        </n-space>
      </n-form-item>
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
  next_date: new Date().toISOString().split('T')[0], // 设置默认日期为今天
  next_date_value: new Date().getTime(), // 使用时间戳作为日期选择器的值
  notify_mode: 'global',
  cust_time: '09:00',
  cust_days: '3,1,0',
  notify_email: true,
  notify_wechat: true,
  notify_webhook: true
})

const cycleOptions = [
  { label: '天', value: 'day' },
  { label: '周', value: 'week' },
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
    // Handle cust_days - it might come as an array from the backend, so convert to comma-separated string for the input
    let custDaysValue = '3,1,0';
    if (props.subscription.cust_days) {
      if (Array.isArray(props.subscription.cust_days)) {
        // If it's an array, join with commas
        custDaysValue = props.subscription.cust_days.join(',');
      } else if (typeof props.subscription.cust_days === 'string') {
        // If it's already a string (comma-separated or JSON string), handle appropriately
        try {
          // Try to parse as JSON to see if it's a JSON array string
          const parsed = JSON.parse(props.subscription.cust_days);
          if (Array.isArray(parsed)) {
            custDaysValue = parsed.join(',');
          } else {
            custDaysValue = props.subscription.cust_days;
          }
        } catch {
          // If not valid JSON, treat as comma-separated string
          custDaysValue = props.subscription.cust_days;
        }
      } else {
        custDaysValue = props.subscription.cust_days;
      }
    }

    formData.value = {
      name: props.subscription.name,
      price: props.subscription.price,
      cycle_val: props.subscription.cycle_val,
      cycle_unit: props.subscription.cycle_unit,
      next_date: props.subscription.next_date,
      next_date_value: props.subscription.next_date ? new Date(props.subscription.next_date).getTime() : new Date().getTime(),
      notify_mode: props.subscription.notify_mode,
      cust_time: props.subscription.cust_time || '09:00',
      cust_days: custDaysValue,
      notify_email: props.subscription.notify_email !== undefined ? props.subscription.notify_email : true,
      notify_wechat: props.subscription.notify_wechat !== undefined ? props.subscription.notify_wechat : true,
      notify_webhook: props.subscription.notify_webhook !== undefined ? props.subscription.notify_webhook : true
    }
    useGlobal.value = props.subscription.notify_mode === 'global'
  } else if (val && !props.subscription) {
    formData.value = {
      name: '',
      price: 0,
      cycle_val: 1,
      cycle_unit: 'month',
      next_date: new Date().toISOString().split('T')[0],
      next_date_value: new Date().getTime(),
      notify_mode: 'global',
      cust_time: '09:00',
      cust_days: '3,1,0',
      notify_email: true,
      notify_wechat: true,
      notify_webhook: true
    }
    useGlobal.value = true
  }
})

watch(show, (val) => {
  emit('update:show', val)
})

const saveSub = async () => {
  try {
    // Convert date value to string format
    if (formData.value.next_date_value) {
      formData.value.next_date = new Date(formData.value.next_date_value).toISOString().split('T')[0];
    }

    // Prepare cust_days as JSON array
    let custDaysValue = null;
    if (!useGlobal.value && formData.value.cust_days) {
      if (typeof formData.value.cust_days === 'string' && formData.value.cust_days.includes(',')) {
        // Convert comma-separated string to array of integers
        const daysArray = formData.value.cust_days.split(',').map(day => {
          const num = parseInt(day.trim(), 10);
          return isNaN(num) ? 0 : num;
        }).filter(num => !isNaN(num));
        custDaysValue = JSON.stringify(daysArray);
      } else if (Array.isArray(formData.value.cust_days)) {
        // If already an array, just stringify it
        custDaysValue = JSON.stringify(formData.value.cust_days);
      } else {
        // Handle single value or other format
        const num = parseInt(formData.value.cust_days, 10);
        custDaysValue = JSON.stringify(isNaN(num) ? [] : [num]);
      }
    }

    const data = {
      ...formData.value,
      notify_mode: useGlobal.value ? 'global' : 'custom',
      cust_time: useGlobal.value ? null : formData.value.cust_time,
      cust_days: useGlobal.value ? null : custDaysValue
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
