<template>
  <div class="dashboard">
    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card" v-for="(stat, index) in stats" :key="stat.label">
        <div class="stat-icon" :class="`stat-icon--${stat.color}`">
          <component :is="stat.icon" />
        </div>
        <div class="stat-label">{{ stat.label }}</div>
        <div class="stat-value">
          <span class="counter" :data-target="stat.value">{{ animatedValues[index] }}</span>
          <span class="stat-unit">{{ stat.unit }}</span>
        </div>
        <div class="stat-trend" :class="stat.trend > 0 ? 'stat-trend--up' : 'stat-trend--down'">
          <svg v-if="stat.trend > 0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
            <polyline points="18 15 12 9 6 15"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
            <polyline points="6 9 12 15 18 9"/>
          </svg>
          {{ Math.abs(stat.trend) }}%
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid--2">
      <!-- Environment Chart Panel -->
      <div class="panel panel--delay-1 grid-span-2">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
            </svg>
            环境数据趋势 · 24小时
          </h3>
          <div class="chart-legend">
            <div class="legend-item">
              <span class="legend-dot legend-dot--emerald"></span>
              温度
            </div>
            <div class="legend-item">
              <span class="legend-dot legend-dot--amber"></span>
              湿度
            </div>
          </div>
        </div>
        <div class="panel-body">
          <div ref="envChartRef" class="chart-container"></div>
        </div>
      </div>

      <!-- Tasks Panel -->
      <div class="panel panel--delay-2">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <path d="M9 11l3 3L22 4"/>
              <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
            </svg>
            待办任务
          </h3>
          <span class="tag tag--warning">{{ pendingTasks.length }} 待处理</span>
        </div>
        <div class="panel-body">
          <div class="timeline">
            <div
              v-for="task in pendingTasks"
              :key="task.id"
              class="timeline-item"
              :class="{ 'timeline-item--completed': task.completed }"
            >
              <div class="timeline-time">{{ task.time }}</div>
              <div class="timeline-content">
                <strong>{{ task.plot }}</strong> - {{ task.action }}
              </div>
            </div>
          </div>
        </div>
        <div class="panel-footer">
          <button class="btn btn--primary btn--sm">
            查看全部任务
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Alerts Panel -->
      <div class="panel panel--delay-3">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            告警中心
          </h3>
          <span class="tag tag--danger">{{ alerts.length }} 条告警</span>
        </div>
        <div class="panel-body">
          <div class="alerts-list">
            <div
              v-for="alert in alerts"
              :key="alert.id"
              class="alert"
              :class="`alert--${alert.type}`"
            >
              <svg class="alert-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              <div class="alert-content">
                <div class="alert-message">{{ alert.message }}</div>
                <div class="alert-time">{{ alert.time }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Crop Distribution -->
      <div class="panel panel--delay-2">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <path d="M21.21 15.89A10 10 0 118 2.83"/>
              <path d="M22 12A10 10 0 0012 2v10z"/>
            </svg>
            作物分布
          </h3>
        </div>
        <div class="panel-body">
          <div ref="cropChartRef" class="chart-container" style="height: 240px;"></div>
        </div>
      </div>

      <!-- Growth Progress -->
      <div class="panel panel--delay-3">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <path d="M12 19V5M5 12l7-7 7 7"/>
            </svg>
            生长进度
          </h3>
        </div>
        <div class="panel-body">
          <div class="growth-list">
            <div v-for="crop in crops" :key="crop.name" class="growth-item">
              <div class="growth-header">
                <span class="growth-name">{{ crop.name }}</span>
                <span class="growth-stage">{{ crop.stage }}</span>
              </div>
              <div class="growth-bar">
                <div class="growth-fill" :style="{ width: `${crop.progress}%` }">
                  <div class="growth-glow"></div>
                </div>
              </div>
              <div class="growth-percent">{{ crop.progress }}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, markRaw } from 'vue'
import * as echarts from 'echarts'

const envChartRef = ref(null)
const cropChartRef = ref(null)

// Animated counter values
const animatedValues = ref([0, 0, 0, 0])

// Icon components
const LeafIcon = markRaw({
  template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 20A7 7 0 019.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>`
})

const SunIcon = markRaw({
  template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>`
})

const DropIcon = markRaw({
  template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z"/></svg>`
})

const PlantIcon = markRaw({
  template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 20h10M10 20c5.5-2.5.8-6.4 3-10M8.5 9.5c2.5 2.5 4.5 6 4.5 10.5M2 12c4.5 2 6 5 6 8"/></svg>`
})

const stats = [
  { label: '种植面积', value: 156, unit: '亩', trend: 8, color: 'emerald', icon: LeafIcon },
  { label: '本月产量', value: 2850, unit: 'kg', trend: 12, color: 'amber', icon: SunIcon },
  { label: '传感器在线', value: 48, unit: '个', trend: 5, color: 'blue', icon: DropIcon },
  { label: '作物种类', value: 8, unit: '种', trend: 0, color: 'rose', icon: PlantIcon }
]

const pendingTasks = [
  { id: 1, plot: '地块A', action: '追施穗肥', time: '今天 14:00', completed: false },
  { id: 2, plot: '温室1', action: '番茄整枝', time: '明天 09:00', completed: false },
  { id: 3, plot: '地块B', action: '除草作业', time: '后天 10:00', completed: false },
  { id: 4, plot: '温室1', action: '灌溉浇水', time: '已完成', completed: true }
]

const alerts = [
  { id: 1, type: 'danger', message: '地块B 土壤湿度过低 (28%)', time: '14:30' },
  { id: 2, type: 'warning', message: '温室1 温度接近上限 (32°C)', time: '13:45' },
  { id: 3, type: 'info', message: '传感器 #12 信号不稳定', time: '10:20' }
]

const crops = [
  { name: '水稻', stage: '孕穗期', progress: 65 },
  { name: '玉米', stage: '拔节期', progress: 40 },
  { name: '番茄', stage: '结果期', progress: 75 },
  { name: '小麦', stage: '分蘖期', progress: 30 }
]

// Animate counters
const animateCounters = () => {
  const duration = 1500
  const steps = 60
  const interval = duration / steps

  stats.forEach((stat, index) => {
    const target = stat.value
    const increment = target / steps
    let current = 0

    const timer = setInterval(() => {
      current += increment
      if (current >= target) {
        current = target
        clearInterval(timer)
      }
      animatedValues.value[index] = Math.round(current)
    }, interval)
  })
}

// Initialize charts
const initEnvChart = () => {
  const chart = echarts.init(envChartRef.value)

  // Generate 24 hours of data
  const hours = Array.from({ length: 24 }, (_, i) => `${i}:00`)
  const tempData = Array.from({ length: 24 }, () => 20 + Math.random() * 12)
  const humidityData = Array.from({ length: 24 }, () => 50 + Math.random() * 30)

  chart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(20, 45, 35, 0.95)',
      borderColor: 'rgba(143, 168, 154, 0.2)',
      textStyle: { color: '#f5f2eb' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: hours,
      axisLine: { lineStyle: { color: 'rgba(143, 168, 154, 0.2)' } },
      axisLabel: { color: '#8fa89a', fontSize: 11 }
    },
    yAxis: [
      {
        type: 'value',
        name: '温度(°C)',
        nameTextStyle: { color: '#8fa89a' },
        axisLine: { show: false },
        splitLine: { lineStyle: { color: 'rgba(143, 168, 154, 0.1)' } },
        axisLabel: { color: '#8fa89a' }
      },
      {
        type: 'value',
        name: '湿度(%)',
        nameTextStyle: { color: '#8fa89a' },
        axisLine: { show: false },
        splitLine: { show: false },
        axisLabel: { color: '#8fa89a' }
      }
    ],
    series: [
      {
        name: '温度',
        type: 'line',
        smooth: true,
        data: tempData,
        itemStyle: { color: '#2ecc71' },
        lineStyle: { width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(46, 204, 113, 0.3)' },
            { offset: 1, color: 'rgba(46, 204, 113, 0)' }
          ])
        },
        animationDuration: 2000,
        animationEasing: 'cubicOut'
      },
      {
        name: '湿度',
        type: 'line',
        smooth: true,
        yAxisIndex: 1,
        data: humidityData,
        itemStyle: { color: '#d4a853' },
        lineStyle: { width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(212, 168, 83, 0.2)' },
            { offset: 1, color: 'rgba(212, 168, 83, 0)' }
          ])
        },
        animationDuration: 2000,
        animationDelay: 300
      }
    ]
  })

  window.addEventListener('resize', () => chart.resize())
}

const initCropChart = () => {
  const chart = echarts.init(cropChartRef.value)

  chart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}亩 ({d}%)',
      backgroundColor: 'rgba(20, 45, 35, 0.95)',
      borderColor: 'rgba(143, 168, 154, 0.2)',
      textStyle: { color: '#f5f2eb' }
    },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#0a1f14',
        borderWidth: 3
      },
      label: {
        show: true,
        color: '#c9c4b8',
        fontSize: 12,
        formatter: '{b}\n{d}%'
      },
      labelLine: {
        lineStyle: { color: 'rgba(143, 168, 154, 0.3)' }
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 20,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
      data: [
        { value: 60, name: '水稻', itemStyle: { color: '#2ecc71' } },
        { value: 45, name: '玉米', itemStyle: { color: '#d4a853' } },
        { value: 30, name: '小麦', itemStyle: { color: '#8fa89a' } },
        { value: 21, name: '蔬菜', itemStyle: { color: '#3498db' } }
      ],
      animationType: 'scale',
      animationEasing: 'elasticOut',
      animationDuration: 1500
    }]
  })

  window.addEventListener('resize', () => chart.resize())
}

onMounted(async () => {
  await nextTick()

  // Start counter animation
  setTimeout(animateCounters, 300)

  // Initialize charts
  initEnvChart()
  initCropChart()
})
</script>

<style lang="scss" scoped>
.dashboard {
  // Additional dashboard-specific styles
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.alert {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  border-left: 3px solid;

  .alert-content {
    flex: 1;

    .alert-message {
      font-size: 0.9rem;
      color: var(--color-cream);
      margin-bottom: var(--space-xs);
    }

    .alert-time {
      font-size: 0.75rem;
      color: var(--color-mist);
    }
  }

  .alert-icon {
    flex-shrink: 0;
    width: 20px;
    height: 20px;
  }
}

.growth-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.growth-item {
  .growth-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--space-sm);

    .growth-name {
      font-weight: 500;
      color: var(--color-cream);
    }

    .growth-stage {
      font-size: 0.8rem;
      color: var(--color-mist);
    }
  }

  .growth-bar {
    height: 8px;
    background: rgba(143, 168, 154, 0.15);
    border-radius: var(--radius-full);
    overflow: hidden;
    position: relative;

    .growth-fill {
      height: 100%;
      border-radius: var(--radius-full);
      background: linear-gradient(90deg, var(--color-emerald) 0%, var(--color-emerald-light) 100%);
      position: relative;
      transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);

      .growth-glow {
        position: absolute;
        right: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        background: radial-gradient(circle, var(--color-emerald-light) 0%, transparent 70%);
        animation: glowPulse 2s ease-in-out infinite;
      }
    }
  }

  .growth-percent {
    text-align: right;
    font-size: 0.75rem;
    color: var(--color-mist);
    margin-top: var(--space-xs);
  }
}

@keyframes glowPulse {
  0%, 100% {
    opacity: 0.5;
    transform: translateY(-50%) scale(1);
  }
  50% {
    opacity: 1;
    transform: translateY(-50%) scale(1.5);
  }
}
</style>
