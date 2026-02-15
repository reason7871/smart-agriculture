<template>
  <div class="settings-page">
    <div class="grid grid--2">
      <!-- 基本设置 -->
      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/>
            </svg>
            基本设置
          </h3>
        </div>
        <div class="panel-body">
          <div class="form-group">
            <label class="form-label">系统名称</label>
            <input v-model="settings.systemName" type="text" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">管理员邮箱</label>
            <input v-model="settings.adminEmail" type="email" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">数据刷新间隔</label>
            <select v-model="settings.refreshInterval" class="form-input form-select">
              <option value="30">30 秒</option>
              <option value="60">1 分钟</option>
              <option value="300">5 分钟</option>
              <option value="600">10 分钟</option>
            </select>
          </div>
        </div>
      </div>

      <!-- 通知设置 -->
      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 01-3.46 0"/>
            </svg>
            通知设置
          </h3>
        </div>
        <div class="panel-body">
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">系统告警通知</div>
              <div class="setting-desc">当传感器数据异常时发送通知</div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.alertNotify" />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">任务提醒</div>
              <div class="setting-desc">农事任务到期前提醒</div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.taskRemind" />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">病虫害识别结果</div>
              <div class="setting-desc">识别完成后显示通知</div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.diseaseNotify" />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-name">邮件通知</div>
              <div class="setting-desc">通过邮件接收重要通知</div>
            </div>
            <label class="toggle">
              <input type="checkbox" v-model="settings.emailNotify" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- 告警阈值 -->
      <div class="panel grid-span-2">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            告警阈值设置
          </h3>
        </div>
        <div class="panel-body">
          <div class="threshold-grid">
            <div class="threshold-item">
              <div class="threshold-header">
                <span class="threshold-icon" style="background: rgba(240, 184, 86, 0.2); color: var(--color-amber);">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                    <circle cx="12" cy="12" r="4"/>
                    <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2"/>
                  </svg>
                </span>
                <span>温度告警</span>
              </div>
              <div class="threshold-inputs">
                <div class="input-group">
                  <label>最低值</label>
                  <input v-model.number="thresholds.tempMin" type="number" class="form-input" />
                  <span>°C</span>
                </div>
                <div class="input-group">
                  <label>最高值</label>
                  <input v-model.number="thresholds.tempMax" type="number" class="form-input" />
                  <span>°C</span>
                </div>
              </div>
            </div>

            <div class="threshold-item">
              <div class="threshold-header">
                <span class="threshold-icon" style="background: rgba(79, 163, 209, 0.2); color: var(--color-info);">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                    <path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z"/>
                  </svg>
                </span>
                <span>湿度告警</span>
              </div>
              <div class="threshold-inputs">
                <div class="input-group">
                  <label>最低值</label>
                  <input v-model.number="thresholds.humidityMin" type="number" class="form-input" />
                  <span>%</span>
                </div>
                <div class="input-group">
                  <label>最高值</label>
                  <input v-model.number="thresholds.humidityMax" type="number" class="form-input" />
                  <span>%</span>
                </div>
              </div>
            </div>

            <div class="threshold-item">
              <div class="threshold-header">
                <span class="threshold-icon" style="background: rgba(61, 214, 140, 0.2); color: var(--color-emerald);">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                    <path d="M11 20A7 7 0 019.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>
                  </svg>
                </span>
                <span>土壤pH告警</span>
              </div>
              <div class="threshold-inputs">
                <div class="input-group">
                  <label>最低值</label>
                  <input v-model.number="thresholds.phMin" type="number" step="0.1" class="form-input" />
                </div>
                <div class="input-group">
                  <label>最高值</label>
                  <input v-model.number="thresholds.phMax" type="number" step="0.1" class="form-input" />
                </div>
              </div>
            </div>

            <div class="threshold-item">
              <div class="threshold-header">
                <span class="threshold-icon" style="background: rgba(239, 99, 85, 0.2); color: var(--color-danger);">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                    <path d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1119.5 12H2"/>
                  </svg>
                </span>
                <span>CO2告警</span>
              </div>
              <div class="threshold-inputs">
                <div class="input-group">
                  <label>最低值</label>
                  <input v-model.number="thresholds.co2Min" type="number" class="form-input" />
                  <span>ppm</span>
                </div>
                <div class="input-group">
                  <label>最高值</label>
                  <input v-model.number="thresholds.co2Max" type="number" class="form-input" />
                  <span>ppm</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="panel-footer">
          <button class="btn btn--primary" @click="saveSettings">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
              <path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/>
              <polyline points="17 21 17 13 7 13 7 21"/>
              <polyline points="7 3 7 8 15 8"/>
            </svg>
            保存设置
          </button>
        </div>
      </div>

      <!-- 系统信息 -->
      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="16" x2="12" y2="12"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
            系统信息
          </h3>
        </div>
        <div class="panel-body">
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">系统版本</span>
              <span class="info-value">v1.0.0</span>
            </div>
            <div class="info-item">
              <span class="info-label">后端服务</span>
              <span class="info-value">
                <span class="status-dot"></span>
                运行中
              </span>
            </div>
            <div class="info-item">
              <span class="info-label">数据库</span>
              <span class="info-value">SQLite</span>
            </div>
            <div class="info-item">
              <span class="info-label">最后更新</span>
              <span class="info-value">2026-02-15</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 数据管理 -->
      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
              <ellipse cx="12" cy="5" rx="9" ry="3"/>
              <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
              <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
            </svg>
            数据管理
          </h3>
        </div>
        <div class="panel-body">
          <div class="data-actions">
            <button class="btn btn--secondary" style="width: 100%; justify-content: flex-start;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              导出所有数据
            </button>
            <button class="btn btn--secondary" style="width: 100%; justify-content: flex-start;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              导入数据
            </button>
            <button class="btn btn--ghost" style="width: 100%; justify-content: flex-start; color: var(--color-danger);">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
              </svg>
              清除缓存数据
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const settings = ref({
  systemName: '智慧农业管理系统',
  adminEmail: 'admin@example.com',
  refreshInterval: '60',
  alertNotify: true,
  taskRemind: true,
  diseaseNotify: true,
  emailNotify: false
})

const thresholds = ref({
  tempMin: 10,
  tempMax: 35,
  humidityMin: 30,
  humidityMax: 85,
  phMin: 5.5,
  phMax: 7.5,
  co2Min: 300,
  co2Max: 1000
})

const saveSettings = () => {
  alert('设置已保存')
}
</script>

<style lang="scss" scoped>
.settings-page {
  .setting-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-md) 0;
    border-bottom: var(--border-subtle);

    &:last-child {
      border-bottom: none;
    }

    .setting-info {
      .setting-name {
        font-weight: 500;
        color: var(--color-cream);
      }

      .setting-desc {
        font-size: 0.8rem;
        color: var(--color-mist);
        margin-top: 2px;
      }
    }
  }
}

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

.threshold-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-xl);

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
}

.threshold-item {
  .threshold-header {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
    font-weight: 500;

    .threshold-icon {
      width: 36px;
      height: 36px;
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }

  .threshold-inputs {
    display: flex;
    gap: var(--space-lg);

    .input-group {
      flex: 1;
      display: flex;
      align-items: center;
      gap: var(--space-sm);

      label {
        font-size: 0.8rem;
        color: var(--color-mist);
        min-width: 50px;
      }

      input {
        width: 80px;
        text-align: center;
      }

      span {
        font-size: 0.85rem;
        color: var(--color-mist);
      }
    }
  }
}

.info-list {
  .info-item {
    display: flex;
    justify-content: space-between;
    padding: var(--space-sm) 0;
    border-bottom: var(--border-subtle);

    &:last-child {
      border-bottom: none;
    }

    .info-label {
      color: var(--color-mist);
    }

    .info-value {
      color: var(--color-cream);
      display: flex;
      align-items: center;
      gap: var(--space-sm);

      .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--color-success);
        animation: pulse 2s infinite;
      }
    }
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.data-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}
</style>
