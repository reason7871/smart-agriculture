<template>
  <div class="analysis-page">
    <!-- Key Stats -->
    <div class="stats-grid">
      <div class="stat-card" v-for="stat in keyStats" :key="stat.label">
        <div class="stat-icon" :class="`stat-icon--${stat.color}`">
          <component :is="stat.icon" />
        </div>
        <div class="stat-label">{{ stat.label }}</div>
        <div class="stat-value">{{ stat.value }}<span class="stat-unit">{{ stat.unit }}</span></div>
        <div class="stat-trend" :class="stat.trend > 0 ? 'stat-trend--up' : 'stat-trend--down'">
          <svg v-if="stat.trend > 0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><polyline points="18 15 12 9 6 15"/></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><polyline points="6 9 12 15 18 9"/></svg>
          {{ Math.abs(stat.trend) }}% 较上季
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="panel" style="margin-bottom: var(--space-lg);">
      <div class="panel-body" style="padding: var(--space-md) var(--space-xl);">
        <div class="filter-row">
          <div class="form-group" style="margin: 0;">
            <label class="form-label">时间范围</label>
            <input type="date" v-model="dateStart" class="form-input" style="width: 140px;" />
            <span style="margin: 0 var(--space-sm); color: var(--color-mist);">至</span>
            <input type="date" v-model="dateEnd" class="form-input" style="width: 140px;" />
          </div>
          <div class="form-group" style="margin: 0;">
            <label class="form-label">预测作物</label>
            <select v-model="selectedCrop" class="form-input form-select" style="width: 140px;" @change="fetchForecast">
              <option value="水稻">水稻</option>
              <option value="玉米">玉米</option>
              <option value="蔬菜">蔬菜</option>
              <option value="小麦">小麦</option>
            </select>
          </div>
          <div class="form-group" style="margin: 0;">
            <label class="form-label">预测期数</label>
            <select v-model="forecastPeriods" class="form-input form-select" style="width: 100px;" @change="fetchForecast">
              <option :value="3">3个月</option>
              <option :value="6">6个月</option>
              <option :value="12">12个月</option>
            </select>
          </div>
          <button class="btn btn--secondary" style="margin-top: auto;" @click="refreshData">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
              <path d="M21 12a9 9 0 11-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/>
              <path d="M21 3v5h-5"/>
            </svg>
            刷新数据
          </button>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div class="grid grid--2">
      <div class="panel grid-span-2">
        <div class="panel-header">
          <h3 class="panel-title">产量趋势分析</h3>
          <div class="btn-group">
            <button v-for="t in ['month', 'quarter', 'year']" :key="t" class="btn btn--sm" :class="chartType === t ? 'btn--primary' : 'btn--ghost'" @click="chartType = t">
              {{ t === 'month' ? '按月' : t === 'quarter' ? '按季' : '按年' }}
            </button>
          </div>
        </div>
        <div class="panel-body">
          <div ref="productionChartRef" class="chart-container"></div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">作物产量占比</h3>
        </div>
        <div class="panel-body">
          <div ref="pieChartRef" class="chart-container" style="height: 280px;"></div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">
            产量预测
            <span v-if="forecastLoading" class="loading-indicator">计算中...</span>
          </h3>
          <div class="algorithm-badge" @click="showAlgorithmInfo = true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="16" x2="12" y2="12"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
            集成模型
          </div>
        </div>
        <div class="panel-body">
          <div ref="forecastChartRef" class="chart-container" style="height: 200px;"></div>
          <div class="forecast-stats" v-if="forecastData">
            <div class="forecast-item">
              <span class="label">预计总产量</span>
              <span class="value">{{ forecastData.summary.total_predicted_yield.toLocaleString() }} kg</span>
            </div>
            <div class="forecast-item">
              <span class="label">预测区间</span>
              <span class="value">{{ forecastData.summary.prediction_range[0].toLocaleString() }} - {{ forecastData.summary.prediction_range[1].toLocaleString() }} kg</span>
            </div>
            <div class="forecast-item">
              <span class="label">置信度</span>
              <span class="value">{{ (forecastData.summary.overall_confidence * 100).toFixed(0) }}%</span>
            </div>
          </div>
          <div class="forecast-stats" v-else>
            <div class="forecast-item"><span class="label">预计产量</span><span class="value">--</span></div>
            <div class="forecast-item"><span class="label">预测区间</span><span class="value">--</span></div>
            <div class="forecast-item"><span class="label">置信度</span><span class="value">--</span></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Prediction Details -->
    <div class="panel" style="margin-top: var(--space-lg);" v-if="forecastData">
      <div class="panel-header">
        <h3 class="panel-title">分月预测详情</h3>
      </div>
      <div class="panel-body" style="padding: 0;">
        <table class="data-table">
          <thead>
            <tr>
              <th>预测期</th>
              <th>预测产量</th>
              <th>置信区间</th>
              <th>趋势</th>
              <th>置信度</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pred in forecastData.predictions" :key="pred.period">
              <td class="cell-value">第 {{ pred.period }} 个月</td>
              <td class="cell-value">{{ pred.predicted_yield.toLocaleString() }} kg</td>
              <td>{{ pred.confidence_lower.toLocaleString() }} - {{ pred.confidence_upper.toLocaleString() }} kg</td>
              <td>
                <span :class="['trend-badge', `trend-badge--${pred.trend}`]">
                  <svg v-if="pred.trend === 'up'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><polyline points="18 15 12 9 6 15"/></svg>
                  <svg v-else-if="pred.trend === 'down'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><polyline points="6 9 12 15 18 9"/></svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12"><line x1="5" y1="12" x2="19" y2="12"/></svg>
                  {{ pred.trend === 'up' ? '上升' : pred.trend === 'down' ? '下降' : '平稳' }}
                </span>
              </td>
              <td>{{ (pred.confidence_level * 100).toFixed(0) }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Historical Data Table -->
    <div class="panel" style="margin-top: var(--space-lg);">
      <div class="panel-header">
        <h3 class="panel-title">历史数据</h3>
      </div>
      <div class="panel-body" style="padding: 0;">
        <table class="data-table">
          <thead>
            <tr><th>周期</th><th>作物</th><th>面积</th><th>产量</th><th>亩产</th><th>成本</th><th>收入</th><th>利润</th></tr>
          </thead>
          <tbody>
            <tr v-for="row in tableData" :key="row.period + row.crop">
              <td class="cell-value">{{ row.period }}</td>
              <td>{{ row.crop }}</td>
              <td>{{ row.area }}亩</td>
              <td class="cell-value">{{ row.production.toLocaleString() }}kg</td>
              <td>{{ row.yield }}kg</td>
              <td>¥{{ row.cost.toLocaleString() }}</td>
              <td>¥{{ row.revenue.toLocaleString() }}</td>
              <td :class="row.profit > 0 ? 'cell-positive' : 'cell-negative'">¥{{ row.profit.toLocaleString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Algorithm Info Modal -->
    <div v-if="showAlgorithmInfo" class="modal-overlay" @click.self="showAlgorithmInfo = false">
      <div class="modal modal--lg">
        <div class="modal-header">
          <h3>预测算法说明</h3>
          <button class="btn btn--ghost btn--sm" @click="showAlgorithmInfo = false">×</button>
        </div>
        <div class="modal-body">
          <div class="algorithm-info">
            <h4>集成预测模型 (Ensemble Forecasting)</h4>
            <p>本系统采用集成学习方法，组合多种预测算法以提高预测准确性。</p>

            <div class="algorithm-components">
              <div class="component-item" v-for="(comp, name) in algorithmComponents" :key="name">
                <div class="component-header">
                  <span class="component-name">{{ comp.name }}</span>
                  <span class="component-weight">权重: {{ (comp.weight * 100).toFixed(0) }}%</span>
                </div>
                <p class="component-desc">{{ comp.description }}</p>
              </div>
            </div>

            <div class="factors-section">
              <h4>考虑因素</h4>
              <div class="factors-grid">
                <div class="factor-item" v-for="factor in consideredFactors" :key="factor.name">
                  <span class="factor-name">{{ factor.description }}</span>
                  <span class="factor-optimal" v-if="factor.optimal_range">最优: {{ factor.optimal_range }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn--primary" @click="showAlgorithmInfo = false">了解了</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, markRaw, computed } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

const dateStart = ref('')
const dateEnd = ref('')
const selectedCrop = ref('水稻')
const forecastPeriods = ref(3)
const chartType = ref('month')
const showAlgorithmInfo = ref(false)

const productionChartRef = ref(null)
const pieChartRef = ref(null)
const forecastChartRef = ref(null)

const forecastData = ref(null)
const forecastLoading = ref(false)
const algorithmInfo = ref(null)

const TrendIcon = markRaw({ template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>` })
const CoinIcon = markRaw({ template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 100 4h4a2 2 0 110 4H8"/><path d="M12 18V6"/></svg>` })
const LeafIcon = markRaw({ template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 20A7 7 0 019.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/></svg>` })
const ChartIcon = markRaw({ template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>` })

const keyStats = ref([
  { label: '总产量', value: '12,500', unit: 'kg', trend: 12, color: 'emerald', icon: LeafIcon },
  { label: '平均亩产', value: '2,500', unit: 'kg', trend: 8, color: 'amber', icon: ChartIcon },
  { label: '总投入', value: '8,500', unit: '元', trend: -5, color: 'blue', icon: CoinIcon },
  { label: '预计收益', value: '32,000', unit: '元', trend: 15, color: 'rose', icon: TrendIcon }
])

const tableData = ref([
  { period: '2026年Q1', crop: '水稻', area: 5, production: 12500, yield: 2500, cost: 3500, revenue: 15000, profit: 11500 },
  { period: '2025年Q4', crop: '玉米', area: 3, production: 5400, yield: 1800, cost: 1800, revenue: 6480, profit: 4680 },
  { period: '2025年Q3', crop: '水稻', area: 5, production: 11200, yield: 2240, cost: 3200, revenue: 13440, profit: 10240 },
  { period: '2025年Q2', crop: '蔬菜', area: 1, production: 2000, yield: 2000, cost: 1200, revenue: 4000, profit: 2800 }
])

const algorithmComponents = computed(() => {
  if (!algorithmInfo.value?.data?.components) {
    return {
      ma: { name: '移动平均预测器', weight: 0.15, description: '基于近期数据的算术平均，适用于短期预测' },
      es: { name: '指数平滑预测器', weight: 0.30, description: '对近期数据赋予更高权重，捕捉趋势变化' },
      seasonal: { name: '季节性预测器', weight: 0.35, description: '识别并利用农业生产的季节性规律' },
      mf: { name: '多因素预测器', weight: 0.20, description: '综合考虑温度、降雨、施肥等环境因素' }
    }
  }
  const result = {}
  algorithmInfo.value.data.components.forEach((comp, i) => {
    result[i] = { name: comp.name, weight: comp.weight, description: comp.description }
  })
  return result
})

const consideredFactors = computed(() => {
  if (!algorithmInfo.value?.data?.factors_considered) {
    return [
      { name: 'temperature', description: '环境温度', optimal_range: '20-30°C' },
      { name: 'rainfall', description: '月降雨量', optimal_range: '100-200mm' },
      { name: 'fertilizer', description: '施肥量', optimal_range: null },
      { name: 'soil_ph', description: '土壤酸碱度', optimal_range: '6.0-7.0' },
      { name: 'sunshine', description: '日照时长', optimal_range: null }
    ]
  }
  return algorithmInfo.value.data.factors_considered
})

let productionChart = null
let forecastChartInstance = null

const fetchForecast = async () => {
  forecastLoading.value = true
  try {
    const response = await axios.get(`${API_BASE}/forecast/predict`, {
      params: {
        crop: selectedCrop.value,
        periods: forecastPeriods.value
      }
    })
    if (response.data.success) {
      forecastData.value = response.data.data
      updateForecastChart()
    }
  } catch (error) {
    console.error('获取预测数据失败:', error)
  } finally {
    forecastLoading.value = false
  }
}

const fetchAlgorithmInfo = async () => {
  try {
    const response = await axios.get(`${API_BASE}/forecast/algorithm/info`)
    if (response.data.success) {
      algorithmInfo.value = response.data
    }
  } catch (error) {
    console.error('获取算法信息失败:', error)
  }
}

const updateForecastChart = () => {
  if (!forecastChartInstance || !forecastData.value) return

  const predictions = forecastData.value.predictions
  const months = predictions.map((_, i) => `${i + 1}月后`)
  const predictedValues = predictions.map(p => p.predicted_yield)
  const lowerBounds = predictions.map(p => p.confidence_lower)
  const upperBounds = predictions.map(p => p.confidence_upper)

  forecastChartInstance.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(20, 45, 35, 0.95)',
      borderColor: 'rgba(143, 168, 154, 0.2)',
      textStyle: { color: '#f5f2eb' },
      formatter: (params) => {
        const data = predictions[params[0].dataIndex]
        return `
          <div style="padding: 4px;">
            <div style="font-weight: 600; margin-bottom: 4px;">${params[0].axisValue}</div>
            <div>预测产量: ${data.predicted_yield.toLocaleString()} kg</div>
            <div>置信区间: ${data.confidence_lower.toLocaleString()} - ${data.confidence_upper.toLocaleString()} kg</div>
            <div>置信度: ${(data.confidence_level * 100).toFixed(0)}%</div>
          </div>
        `
      }
    },
    xAxis: {
      type: 'category',
      data: months,
      axisLine: { lineStyle: { color: 'rgba(143, 168, 154, 0.2)' } },
      axisLabel: { color: '#8fa89a' }
    },
    yAxis: {
      type: 'value',
      name: '产量(kg)',
      nameTextStyle: { color: '#8fa89a' },
      axisLine: { show: false },
      splitLine: { lineStyle: { color: 'rgba(143, 168, 154, 0.1)' } },
      axisLabel: { color: '#8fa89a' }
    },
    series: [
      {
        name: '置信区间',
        type: 'line',
        data: upperBounds,
        lineStyle: { opacity: 0 },
        areaStyle: { opacity: 0 },
        stack: 'confidence',
        symbol: 'none'
      },
      {
        name: '区间下限',
        type: 'line',
        data: lowerBounds.map((v, i) => upperBounds[i] - v),
        lineStyle: { opacity: 0 },
        areaStyle: { color: 'rgba(212, 168, 83, 0.15)' },
        stack: 'confidence',
        symbol: 'none'
      },
      {
        name: '预测产量',
        type: 'line',
        data: predictedValues,
        itemStyle: { color: '#d4a853' },
        lineStyle: { width: 3 },
        symbol: 'circle',
        symbolSize: 8,
        emphasis: {
          itemStyle: { borderColor: '#fff', borderWidth: 2 }
        }
      }
    ]
  })
}

const refreshData = () => {
  fetchForecast()
}

const initCharts = () => {
  // Production Chart
  productionChart = echarts.init(productionChartRef.value)
  productionChart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: 'rgba(20, 45, 35, 0.95)', borderColor: 'rgba(143, 168, 154, 0.2)', textStyle: { color: '#f5f2eb' } },
    legend: { data: ['水稻', '玉米', '蔬菜'], textStyle: { color: '#8fa89a' }, top: 0 },
    grid: { left: '3%', right: '4%', bottom: '3%', top: '15%', containLabel: true },
    xAxis: { type: 'category', data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'], axisLine: { lineStyle: { color: 'rgba(143, 168, 154, 0.2)' } }, axisLabel: { color: '#8fa89a' } },
    yAxis: { type: 'value', name: '产量(kg)', nameTextStyle: { color: '#8fa89a' }, axisLine: { show: false }, splitLine: { lineStyle: { color: 'rgba(143, 168, 154, 0.1)' } }, axisLabel: { color: '#8fa89a' } },
    series: [
      { name: '水稻', type: 'bar', data: [0,0,1200,1500,1800,2000,0,0,2500,3000,0,0], itemStyle: { color: '#2ecc71', borderRadius: [4,4,0,0] } },
      { name: '玉米', type: 'bar', data: [0,0,0,0,800,1200,1800,2000,0,0,0,0], itemStyle: { color: '#d4a853', borderRadius: [4,4,0,0] } },
      { name: '蔬菜', type: 'bar', data: [500,600,700,800,900,0,0,0,800,700,600,500], itemStyle: { color: '#3498db', borderRadius: [4,4,0,0] } }
    ]
  })
  window.addEventListener('resize', () => productionChart.resize())

  // Pie Chart
  const pieChart = echarts.init(pieChartRef.value)
  pieChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c}kg ({d}%)', backgroundColor: 'rgba(20, 45, 35, 0.95)', borderColor: 'rgba(143, 168, 154, 0.2)', textStyle: { color: '#f5f2eb' } },
    series: [{
      type: 'pie', radius: ['40%', '70%'], itemStyle: { borderRadius: 6, borderColor: '#0a1f14', borderWidth: 2 },
      label: { show: true, color: '#c9c4b8', formatter: '{b}\n{d}%' },
      data: [{ value: 7500, name: '水稻', itemStyle: { color: '#2ecc71' } }, { value: 3800, name: '玉米', itemStyle: { color: '#d4a853' } }, { value: 1200, name: '蔬菜', itemStyle: { color: '#3498db' } }]
    }]
  })
  window.addEventListener('resize', () => pieChart.resize())

  // Forecast Chart - 初始化空图表
  forecastChartInstance = echarts.init(forecastChartRef.value)
  forecastChartInstance.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', top: '10%', containLabel: true },
    xAxis: { type: 'category', data: [], axisLine: { lineStyle: { color: 'rgba(143, 168, 154, 0.2)' } }, axisLabel: { color: '#8fa89a' } },
    yAxis: { type: 'value', axisLine: { show: false }, splitLine: { lineStyle: { color: 'rgba(143, 168, 154, 0.1)' } }, axisLabel: { color: '#8fa89a' } },
    series: []
  })
  window.addEventListener('resize', () => forecastChartInstance.resize())
}

onMounted(async () => {
  await nextTick()
  initCharts()
  fetchForecast()
  fetchAlgorithmInfo()
})
</script>

<style lang="scss" scoped>
.filter-row {
  display: flex;
  align-items: flex-end;
  gap: var(--space-xl);
}

.btn-group { display: flex; gap: var(--space-xs); }

.loading-indicator {
  font-size: 0.75rem;
  color: var(--color-amber);
  margin-left: var(--space-sm);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.algorithm-badge {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: 0.75rem;
  color: var(--color-mist);
  cursor: pointer;
  padding: var(--space-xs) var(--space-sm);
  background: var(--surface-glass);
  border-radius: var(--radius-sm);
  transition: all var(--duration-fast);

  &:hover {
    color: var(--color-amber);
    background: rgba(240, 184, 86, 0.1);
  }
}

.forecast-stats {
  display: flex;
  justify-content: space-around;
  margin-top: var(--space-lg);
  padding: var(--space-md);
  background: rgba(255,255,255,0.02);
  border-radius: var(--radius-md);

  .forecast-item {
    text-align: center;
    .label { display: block; font-size: 0.75rem; color: var(--color-mist); margin-bottom: 4px; }
    .value { font-size: 1.1rem; font-weight: 600; color: var(--color-cream); }
  }
}

.trend-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: 0.8rem;

  &--up {
    background: rgba(46, 204, 113, 0.15);
    color: var(--color-emerald);
  }

  &--down {
    background: rgba(239, 99, 85, 0.15);
    color: var(--color-danger);
  }

  &--stable {
    background: rgba(143, 168, 154, 0.15);
    color: var(--color-mist);
  }
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--color-moss);
  border-radius: var(--radius-lg);
  border: var(--border-subtle);
  width: 100%;
  max-width: 480px;

  &--lg {
    max-width: 640px;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg) var(--space-xl);
  border-bottom: var(--border-subtle);
  h3 { margin: 0; }
}

.modal-body { padding: var(--space-xl); }
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-md);
  padding: var(--space-lg) var(--space-xl);
  border-top: var(--border-subtle);
}

.algorithm-info {
  h4 {
    color: var(--color-amber);
    margin-bottom: var(--space-sm);
    font-size: 1rem;
  }

  p {
    color: var(--color-cream-muted);
    line-height: 1.6;
    margin-bottom: var(--space-lg);
  }
}

.algorithm-components {
  margin-bottom: var(--space-lg);

  .component-item {
    padding: var(--space-md);
    background: rgba(255,255,255,0.02);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-sm);

    .component-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: var(--space-xs);
    }

    .component-name {
      font-weight: 500;
      color: var(--color-cream);
    }

    .component-weight {
      font-size: 0.8rem;
      color: var(--color-amber);
    }

    .component-desc {
      font-size: 0.85rem;
      color: var(--color-mist);
      margin: 0;
    }
  }
}

.factors-section {
  h4 {
    margin-bottom: var(--space-md);
  }

  .factors-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-sm);
  }

  .factor-item {
    display: flex;
    justify-content: space-between;
    padding: var(--space-sm);
    background: rgba(255,255,255,0.02);
    border-radius: var(--radius-sm);
    font-size: 0.85rem;

    .factor-name {
      color: var(--color-cream-muted);
    }

    .factor-optimal {
      color: var(--color-mist);
      font-size: 0.8rem;
    }
  }
}
</style>
