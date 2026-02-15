<template>
  <div class="monitor-page">
    <!-- Realtime Stats -->
    <div class="stats-grid">
      <div
        class="stat-card"
        v-for="sensor in realtimeData"
        :key="sensor.type"
        :class="{ 'stat-card--warning': sensor.isWarning }"
      >
        <div class="stat-icon" :class="`stat-icon--${sensor.iconColor}`">
          <component :is="sensor.icon" />
        </div>
        <div class="stat-label">{{ sensor.label }}</div>
        <div class="stat-value">
          {{ sensor.value }}
          <span class="stat-unit">{{ sensor.unit }}</span>
        </div>
        <div class="stat-range">
          正常范围: {{ sensor.min }} - {{ sensor.max }} {{ sensor.unit }}
        </div>
      </div>
    </div>

    <!-- Chart Panel -->
    <div class="panel">
      <div class="panel-header">
        <h3 class="panel-title">
          <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
          </svg>
          历史数据趋势
        </h3>
        <div class="filter-group">
          <select v-model="selectedSensor" class="form-input form-select" style="width: 140px;">
            <option value="temperature">温度</option>
            <option value="humidity">湿度</option>
            <option value="ph">土壤pH</option>
            <option value="light">光照</option>
            <option value="co2">CO2</option>
          </select>
          <div class="btn-group">
            <button
              v-for="range in timeRanges"
              :key="range.value"
              class="btn btn--sm"
              :class="timeRange === range.value ? 'btn--primary' : 'btn--ghost'"
              @click="timeRange = range.value"
            >
              {{ range.label }}
            </button>
          </div>
        </div>
      </div>
      <div class="panel-body">
        <div ref="chartRef" class="chart-container"></div>
      </div>
    </div>

    <!-- Sensors List -->
    <div class="grid grid--2" style="margin-top: var(--space-lg);">
      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
              <path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/>
            </svg>
            传感器列表
          </h3>
          <button class="btn btn--primary btn--sm" @click="showAddSensor = true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            添加传感器
          </button>
        </div>
        <div class="panel-body" style="padding: 0;">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>名称</th>
                <th>类型</th>
                <th>位置</th>
                <th>当前值</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sensor in sensors" :key="sensor.id">
                <td class="cell-value">{{ sensor.id }}</td>
                <td>{{ sensor.name }}</td>
                <td>
                  <span class="tag tag--neutral">{{ getSensorTypeLabel(sensor.type) }}</span>
                </td>
                <td>{{ sensor.location }}</td>
                <td :class="{ 'cell-negative': sensor.isWarning }">
                  {{ sensor.value }} {{ sensor.unit }}
                </td>
                <td>
                  <span :class="['tag', sensor.status === 'online' ? 'tag--success' : 'tag--danger']">
                    {{ sensor.status === 'online' ? '在线' : '离线' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            告警规则
          </h3>
        </div>
        <div class="panel-body">
          <div class="rule-list">
            <div v-for="rule in alertRules" :key="rule.id" class="rule-item">
              <div class="rule-info">
                <div class="rule-name">{{ rule.name }}</div>
                <div class="rule-condition">{{ rule.condition }}</div>
              </div>
              <label class="toggle">
                <input type="checkbox" v-model="rule.enabled" />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Sensor Modal -->
    <div v-if="showAddSensor" class="modal-overlay" @click.self="showAddSensor = false">
      <div class="modal">
        <div class="modal-header">
          <h3>添加传感器</h3>
          <button class="btn btn--ghost btn--sm" @click="showAddSensor = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">传感器名称</label>
            <input v-model="sensorForm.name" type="text" class="form-input" placeholder="请输入传感器名称" />
          </div>
          <div class="form-group">
            <label class="form-label">传感器类型</label>
            <select v-model="sensorForm.type" class="form-input form-select">
              <option value="temperature">空气温度</option>
              <option value="humidity">空气湿度</option>
              <option value="ph">土壤pH</option>
              <option value="light">光照强度</option>
              <option value="co2">CO2浓度</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">安装位置</label>
            <input v-model="sensorForm.location" type="text" class="form-input" placeholder="请输入安装位置" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn--secondary" @click="showAddSensor = false">取消</button>
          <button class="btn btn--primary" @click="addSensor">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, markRaw } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref(null)
const selectedSensor = ref('temperature')
const timeRange = ref('24h')
const showAddSensor = ref(false)

const timeRanges = [
  { label: '24小时', value: '24h' },
  { label: '7天', value: '7d' },
  { label: '30天', value: '30d' }
]

// Icons
const SunIcon = markRaw({ template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>` })
const DropIcon = markRaw({ template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z"/></svg>` })
const LeafIcon = markRaw({ template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 20A7 7 0 019.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>` })
const LightIcon = markRaw({ template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>` })
const WindIcon = markRaw({ template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1119.5 12H2"/></svg>` })

const realtimeData = ref([
  { type: 'temperature', label: '空气温度', value: 26.5, unit: '°C', min: 15, max: 35, icon: SunIcon, iconColor: 'amber', isWarning: false },
  { type: 'humidity', label: '空气湿度', value: 68, unit: '%', min: 40, max: 80, icon: DropIcon, iconColor: 'blue', isWarning: false },
  { type: 'ph', label: '土壤pH', value: 6.8, unit: '', min: 5.5, max: 7.5, icon: LeafIcon, iconColor: 'emerald', isWarning: false },
  { type: 'light', label: '光照强度', value: 45000, unit: 'Lux', min: 0, max: 100000, icon: LightIcon, iconColor: 'amber', isWarning: false },
  { type: 'co2', label: 'CO2浓度', value: 650, unit: 'ppm', min: 300, max: 1000, icon: WindIcon, iconColor: 'blue', isWarning: false }
])

const sensors = ref([
  { id: 'S001', name: '温湿度传感器-1', type: 'temperature', location: '地块A', value: 26.5, unit: '°C', status: 'online', isWarning: false },
  { id: 'S002', name: '土壤传感器-1', type: 'ph', location: '地块A', value: 6.8, unit: '', status: 'online', isWarning: false },
  { id: 'S003', name: '光照传感器-1', type: 'light', location: '温室1', value: 45000, unit: 'Lux', status: 'online', isWarning: false },
  { id: 'S004', name: 'CO2传感器-1', type: 'co2', location: '温室1', value: 650, unit: 'ppm', status: 'online', isWarning: false },
  { id: 'S005', name: '温湿度传感器-2', type: 'humidity', location: '地块B', value: 28, unit: '%', status: 'offline', isWarning: true }
])

const alertRules = ref([
  { id: 1, name: '高温告警', condition: '温度 > 35°C', enabled: true },
  { id: 2, name: '低温告警', condition: '温度 < 10°C', enabled: true },
  { id: 3, name: '低湿度告警', condition: '湿度 < 30%', enabled: true },
  { id: 4, name: 'pH异常告警', condition: 'pH < 5.5 或 pH > 7.5', enabled: true }
])

const sensorForm = ref({ name: '', type: 'temperature', location: '' })

const getSensorTypeLabel = (type) => {
  const labels = { temperature: '温度', humidity: '湿度', ph: '土壤pH', light: '光照', co2: 'CO2' }
  return labels[type] || type
}

const addSensor = () => {
  if (!sensorForm.value.name) return
  sensors.value.push({
    id: `S${String(sensors.value.length + 1).padStart(3, '0')}`,
    ...sensorForm.value,
    value: '--',
    unit: '',
    status: 'online',
    isWarning: false
  })
  showAddSensor.value = false
  sensorForm.value = { name: '', type: 'temperature', location: '' }
}

let chart = null

const initChart = () => {
  if (chart) chart.dispose()
  chart = echarts.init(chartRef.value)

  const dataPoints = timeRange.value === '24h' ? 24 : timeRange.value === '7d' ? 7 : 30
  const xData = Array.from({ length: dataPoints }, (_, i) => {
    if (timeRange.value === '24h') return `${i}:00`
    return `第${i + 1}天`
  })

  const baseValues = { temperature: 25, humidity: 60, ph: 6.5, light: 50000, co2: 600 }
  const base = baseValues[selectedSensor.value] || 25
  const data = Array.from({ length: dataPoints }, () => base + (Math.random() - 0.5) * base * 0.3)

  chart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(20, 45, 35, 0.95)', borderColor: 'rgba(143, 168, 154, 0.2)', textStyle: { color: '#f5f2eb' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: xData, axisLine: { lineStyle: { color: 'rgba(143, 168, 154, 0.2)' } }, axisLabel: { color: '#8fa89a' } },
    yAxis: { type: 'value', axisLine: { show: false }, splitLine: { lineStyle: { color: 'rgba(143, 168, 154, 0.1)' } }, axisLabel: { color: '#8fa89a' } },
    series: [{
      type: 'line',
      smooth: true,
      data: data,
      itemStyle: { color: '#2ecc71' },
      lineStyle: { width: 3 },
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(46, 204, 113, 0.3)' }, { offset: 1, color: 'rgba(46, 204, 113, 0)' }]) }
    }]
  })
}

watch([selectedSensor, timeRange], initChart)

onMounted(async () => {
  await nextTick()
  initChart()
  window.addEventListener('resize', () => chart?.resize())
})
</script>

<style lang="scss" scoped>
.monitor-page {
  .stat-card--warning {
    border-left: 3px solid var(--color-warning);
  }

  .filter-group {
    display: flex;
    align-items: center;
    gap: var(--space-md);
  }

  .btn-group {
    display: flex;
    gap: var(--space-xs);
  }

  .rule-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-md);
  }

  .rule-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-md);
    background: rgba(255,255,255,0.02);
    border-radius: var(--radius-md);

    .rule-info {
      .rule-name { font-weight: 500; color: var(--color-cream); }
      .rule-condition { font-size: 0.8rem; color: var(--color-mist); margin-top: 2px; }
    }
  }
}

// Toggle switch
.toggle {
  position: relative;
  width: 44px;
  height: 24px;

  input { opacity: 0; width: 0; height: 0; }

  .toggle-slider {
    position: absolute;
    inset: 0;
    background: var(--surface-glass);
    border-radius: var(--radius-full);
    cursor: pointer;
    transition: background var(--duration-normal);

    &::before {
      content: '';
      position: absolute;
      width: 18px;
      height: 18px;
      left: 3px;
      bottom: 3px;
      background: var(--color-mist);
      border-radius: 50%;
      transition: transform var(--duration-normal);
    }
  }

  input:checked + .toggle-slider {
    background: var(--color-emerald);

    &::before {
      transform: translateX(20px);
      background: var(--color-cream);
    }
  }
}

// Modal
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modal {
  background: var(--color-moss);
  border-radius: var(--radius-lg);
  border: var(--border-subtle);
  width: 100%;
  max-width: 480px;
  animation: slideUp 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg) var(--space-xl);
  border-bottom: var(--border-subtle);

  h3 { margin: 0; font-family: var(--font-display); }
}

.modal-body {
  padding: var(--space-xl);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-md);
  padding: var(--space-lg) var(--space-xl);
  border-top: var(--border-subtle);
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
