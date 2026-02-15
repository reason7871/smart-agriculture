import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 侧边栏折叠状态
  const isCollapse = ref(false)

  // 当前选中的地块
  const selectedPlot = ref(null)

  // 告警数量
  const alertCount = ref(3)

  // 切换侧边栏折叠
  const toggleCollapse = () => {
    isCollapse.value = !isCollapse.value
  }

  // 设置选中地块
  const setSelectedPlot = (plot) => {
    selectedPlot.value = plot
  }

  // 设置告警数量
  const setAlertCount = (count) => {
    alertCount.value = count
  }

  return {
    isCollapse,
    selectedPlot,
    alertCount,
    toggleCollapse,
    setSelectedPlot,
    setAlertCount
  }
})

export const useSensorStore = defineStore('sensor', () => {
  // 传感器列表
  const sensors = ref([])

  // 实时数据
  const realtimeData = ref({})

  // 告警规则
  const alertRules = ref([])

  const setSensors = (data) => {
    sensors.value = data
  }

  const setRealtimeData = (data) => {
    realtimeData.value = data
  }

  const setAlertRules = (rules) => {
    alertRules.value = rules
  }

  return {
    sensors,
    realtimeData,
    alertRules,
    setSensors,
    setRealtimeData,
    setAlertRules
  }
})

export const useCropStore = defineStore('crop', () => {
  // 地块列表
  const plots = ref([])

  // 农事任务
  const tasks = ref([])

  // 作物类型
  const cropTypes = ref([
    { value: 'rice', label: '水稻', growthStages: ['播种', '发芽', '秧苗', '分蘖', '孕穗', '抽穗', '成熟'] },
    { value: 'corn', label: '玉米', growthStages: ['播种', '出苗', '拔节', '抽雄', '开花', '灌浆', '成熟'] },
    { value: 'wheat', label: '小麦', growthStages: ['播种', '出苗', '分蘖', '拔节', '孕穗', '抽穗', '成熟'] },
    { value: 'vegetable', label: '蔬菜', growthStages: ['播种', '发芽', '幼苗', '生长期', '开花', '结果', '收获'] }
  ])

  const setPlots = (data) => {
    plots.value = data
  }

  const setTasks = (data) => {
    tasks.value = data
  }

  return {
    plots,
    tasks,
    cropTypes,
    setPlots,
    setTasks
  }
})
