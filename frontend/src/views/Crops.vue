<template>
  <div class="crops-page">
    <!-- Plots Grid -->
    <div class="panel">
      <div class="panel-header">
        <h3 class="panel-title">
          <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
            <rect x="3" y="3" width="7" height="7"/>
            <rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/>
          </svg>
          地块管理
        </h3>
        <button class="btn btn--primary btn--sm" @click="showAddPlot = true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          新增地块
        </button>
      </div>
      <div class="panel-body">
        <div class="plots-grid">
          <div
            v-for="plot in plots"
            :key="plot.id"
            class="plot-card"
            :class="{ 'plot-card--selected': selectedPlot?.id === plot.id }"
            @click="selectPlot(plot)"
          >
            <div class="plot-header">
              <span class="plot-name">{{ plot.name }}</span>
              <div class="plot-header-actions">
                <span :class="['tag', plot.status === '种植中' ? 'tag--success' : 'tag--neutral']">
                  {{ plot.status }}
                </span>
                <button class="btn btn--ghost btn--sm plot-delete-btn" @click.stop="confirmDeletePlot(plot)" title="删除地块">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                    <polyline points="3 6 5 6 21 6"/>
                    <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="plot-info">
              <div class="info-row">
                <span class="info-label">面积</span>
                <span class="info-value">{{ plot.area }} 亩</span>
              </div>
              <div class="info-row">
                <span class="info-label">作物</span>
                <span class="info-value">{{ plot.crop || '未种植' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">阶段</span>
                <span class="info-value">{{ plot.growthStage || '--' }}</span>
              </div>
            </div>
            <div v-if="plot.crop" class="plot-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${plot.progress}%` }"></div>
              </div>
              <span class="progress-label">生长进度 {{ plot.progress }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Plot Details -->
    <div v-if="selectedPlot" class="grid grid--2" style="margin-top: var(--space-lg);">
      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">{{ selectedPlot.name }} - 农事记录</h3>
          <button class="btn btn--secondary btn--sm" @click="showAddTask = true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            添加任务
          </button>
        </div>
        <div class="panel-body" style="padding: 0;">
          <table class="data-table">
            <thead>
              <tr>
                <th>日期</th>
                <th>类型</th>
                <th>描述</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in farmingTasks" :key="task.id">
                <td>{{ task.date }}</td>
                <td>
                  <span :class="['tag', getTaskTagType(task.type)]">{{ task.type }}</span>
                </td>
                <td>{{ task.description }}</td>
                <td>
                  <span :class="['tag', task.status === 'completed' ? 'tag--success' : 'tag--warning']">
                    {{ task.status === 'completed' ? '已完成' : '待办' }}
                  </span>
                </td>
                <td>
                  <button
                    v-if="task.status !== 'completed'"
                    class="btn btn--ghost btn--sm"
                    @click="completeTask(task)"
                  >
                    完成
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">生长时间线</h3>
        </div>
        <div class="panel-body">
          <div class="timeline">
            <div
              v-for="(stage, index) in growthStages"
              :key="index"
              class="timeline-item"
              :class="{ 'timeline-item--completed': stage.completed }"
            >
              <div class="timeline-content">
                <strong>{{ stage.name }}</strong>
                <span v-if="stage.date" class="timeline-date">{{ stage.date }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Plot Modal -->
    <div v-if="showAddPlot" class="modal-overlay" @click.self="showAddPlot = false">
      <div class="modal">
        <div class="modal-header">
          <h3>新增地块</h3>
          <button class="btn btn--ghost btn--sm" @click="showAddPlot = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">地块名称</label>
            <input v-model="plotForm.name" type="text" class="form-input" placeholder="请输入地块名称" />
          </div>
          <div class="form-group">
            <label class="form-label">面积(亩)</label>
            <input v-model.number="plotForm.area" type="number" class="form-input" step="0.1" />
          </div>
          <div class="form-group">
            <label class="form-label">位置</label>
            <input v-model="plotForm.location" type="text" class="form-input" placeholder="请输入位置描述" />
          </div>
          <div class="form-group">
            <label class="form-label">土壤类型</label>
            <select v-model="plotForm.soilType" class="form-input form-select">
              <option value="沙土">沙土</option>
              <option value="壤土">壤土</option>
              <option value="粘土">粘土</option>
              <option value="沙壤土">沙壤土</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn--secondary" @click="showAddPlot = false">取消</button>
          <button class="btn btn--primary" @click="addPlot">确定</button>
        </div>
      </div>
    </div>

    <!-- Delete Confirm Modal -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click.self="showDeleteConfirm = false">
      <div class="modal modal--danger">
        <div class="modal-header">
          <h3>确认删除</h3>
          <button class="btn btn--ghost btn--sm" @click="showDeleteConfirm = false">×</button>
        </div>
        <div class="modal-body">
          <div class="delete-warning">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="48" height="48">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <p>确定要删除地块 <strong>{{ plotToDelete?.name }}</strong> 吗？</p>
            <p class="delete-hint">此操作不可撤销，该地块的所有数据将被永久删除。</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn--secondary" @click="showDeleteConfirm = false">取消</button>
          <button class="btn btn--danger" @click="deletePlot">确认删除</button>
        </div>
      </div>
    </div>

    <!-- Add Task Modal -->
    <div v-if="showAddTask" class="modal-overlay" @click.self="showAddTask = false">
      <div class="modal">
        <div class="modal-header">
          <h3>添加农事任务</h3>
          <button class="btn btn--ghost btn--sm" @click="showAddTask = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">任务类型</label>
            <select v-model="taskForm.type" class="form-input form-select">
              <option value="播种">播种</option>
              <option value="施肥">施肥</option>
              <option value="浇水">浇水</option>
              <option value="除草">除草</option>
              <option value="喷药">喷药</option>
              <option value="收获">收获</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">计划日期</label>
            <input v-model="taskForm.date" type="date" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">描述</label>
            <textarea v-model="taskForm.description" class="form-input" rows="3" placeholder="请输入任务描述"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn--secondary" @click="showAddTask = false">取消</button>
          <button class="btn btn--primary" @click="addTask">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showAddPlot = ref(false)
const showAddTask = ref(false)
const showDeleteConfirm = ref(false)
const selectedPlot = ref(null)
const plotToDelete = ref(null)

const plots = ref([
  { id: 1, name: '地块A', area: 5, location: '东部', soilType: '壤土', crop: '水稻', growthStage: '孕穗期', status: '种植中', progress: 65 },
  { id: 2, name: '地块B', area: 3, location: '西部', soilType: '沙壤土', crop: '玉米', growthStage: '拔节期', status: '种植中', progress: 40 },
  { id: 3, name: '温室1', area: 1, location: '北部', soilType: '壤土', crop: '番茄', growthStage: '结果期', status: '种植中', progress: 75 },
  { id: 4, name: '地块C', area: 4, location: '南部', soilType: '粘土', crop: null, growthStage: null, status: '空闲', progress: 0 }
])

const farmingTasks = ref([
  { id: 1, date: '2026-02-14', type: '施肥', description: '追施尿素10kg/亩', status: 'completed' },
  { id: 2, date: '2026-02-16', type: '喷药', description: '防治稻瘟病', status: 'pending' },
  { id: 3, date: '2026-02-18', type: '浇水', description: '灌溉一次', status: 'pending' }
])

const growthStages = ref([
  { name: '播种', completed: true, date: '2026-01-15' },
  { name: '发芽', completed: true, date: '2026-01-22' },
  { name: '秧苗期', completed: true, date: '2026-02-01' },
  { name: '分蘖期', completed: true, date: '2026-02-10' },
  { name: '孕穗期', completed: false, date: null },
  { name: '抽穗期', completed: false, date: null },
  { name: '成熟期', completed: false, date: null },
  { name: '收获', completed: false, date: null }
])

const plotForm = ref({ name: '', area: 1, location: '', soilType: '壤土' })
const taskForm = ref({ type: '施肥', date: '', description: '' })

const getTaskTagType = (type) => {
  const types = { '播种': 'tag--info', '施肥': 'tag--warning', '浇水': 'tag--info', '除草': 'tag--success', '喷药': 'tag--danger', '收获': 'tag--success' }
  return types[type] || 'tag--neutral'
}

const selectPlot = (plot) => { selectedPlot.value = plot }
const addPlot = () => {
  if (!plotForm.value.name) return
  plots.value.push({ id: plots.value.length + 1, ...plotForm.value, crop: null, growthStage: null, status: '空闲', progress: 0 })
  showAddPlot.value = false
  plotForm.value = { name: '', area: 1, location: '', soilType: '壤土' }
}
const addTask = () => {
  if (!taskForm.value.date) return
  farmingTasks.value.unshift({ id: farmingTasks.value.length + 1, ...taskForm.value, status: 'pending' })
  showAddTask.value = false
  taskForm.value = { type: '施肥', date: '', description: '' }
}
const completeTask = (task) => { task.status = 'completed' }

const confirmDeletePlot = (plot) => {
  plotToDelete.value = plot
  showDeleteConfirm.value = true
}

const deletePlot = () => {
  if (!plotToDelete.value) return
  const index = plots.value.findIndex(p => p.id === plotToDelete.value.id)
  if (index !== -1) {
    plots.value.splice(index, 1)
    if (selectedPlot.value?.id === plotToDelete.value.id) {
      selectedPlot.value = null
    }
  }
  showDeleteConfirm.value = false
  plotToDelete.value = null
}
</script>

<style lang="scss" scoped>
.plots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-lg);
}

.plot-card {
  background: rgba(255,255,255,0.02);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  cursor: pointer;
  border: 2px solid transparent;
  transition: all var(--duration-normal);

  &:hover {
    background: rgba(255,255,255,0.04);
    border-color: rgba(46, 204, 113, 0.3);
  }

  &.plot-card--selected {
    border-color: var(--color-emerald);
    background: rgba(46, 204, 113, 0.05);
  }

  .plot-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-md);

    .plot-name {
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--color-cream);
    }

    .plot-header-actions {
      display: flex;
      align-items: center;
      gap: var(--space-sm);
    }

    .plot-delete-btn {
      padding: 4px;
      opacity: 0;
      transition: opacity var(--duration-fast), color var(--duration-fast);

      &:hover {
        color: var(--color-danger);
      }
    }
  }

  &:hover .plot-delete-btn {
    opacity: 1;
  }

  .plot-info {
    margin-bottom: var(--space-md);

    .info-row {
      display: flex;
      justify-content: space-between;
      padding: var(--space-xs) 0;

      .info-label { color: var(--color-mist); font-size: 0.9rem; }
      .info-value { color: var(--color-cream-muted); font-size: 0.9rem; }
    }
  }

  .plot-progress {
    .progress-bar {
      height: 6px;
      background: rgba(143, 168, 154, 0.15);
      border-radius: var(--radius-full);
      overflow: hidden;
      margin-bottom: var(--space-xs);

      .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--color-emerald), var(--color-emerald-light));
        border-radius: var(--radius-full);
        transition: width 0.6s ease;
      }
    }

    .progress-label {
      font-size: 0.75rem;
      color: var(--color-mist);
    }
  }
}

.timeline-date {
  font-size: 0.8rem;
  color: var(--color-mist);
  margin-left: var(--space-sm);
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

.modal--danger {
  .modal-header h3 {
    color: var(--color-danger);
  }
}

.delete-warning {
  text-align: center;
  padding: var(--space-lg) 0;

  svg {
    color: var(--color-danger);
    margin-bottom: var(--space-md);
  }

  p {
    color: var(--color-cream-muted);
    margin-bottom: var(--space-sm);

    strong {
      color: var(--color-cream);
    }
  }

  .delete-hint {
    font-size: 0.85rem;
    color: var(--color-mist);
  }
}

.btn--danger {
  background: var(--color-danger);
  color: white;
  border: none;

  &:hover {
    background: #c0392b;
  }
}
</style>
