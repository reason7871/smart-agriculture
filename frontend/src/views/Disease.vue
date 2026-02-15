<template>
  <div class="disease-page">
    <div class="grid grid--2">
      <!-- Upload Section -->
      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">上传图片识别</h3>
        </div>
        <div class="panel-body">
          <div
            class="upload-zone"
            :class="{ 'upload-zone--dragover': isDragover }"
            @dragover.prevent="isDragover = true"
            @dragleave="isDragover = false"
            @drop.prevent="handleDrop"
            @click="triggerUpload"
          >
            <input ref="fileInput" type="file" accept="image/*" hidden @change="handleFileSelect" />
            <div v-if="!previewImage" class="upload-placeholder">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="48" height="48">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              <div class="upload-text">
                <span>拖拽图片到此处或</span>
                <em>点击上传</em>
              </div>
              <div class="upload-hint">支持 JPG、PNG 格式，大小不超过 5MB</div>
            </div>
            <div v-else class="upload-preview">
              <img :src="previewImage" alt="预览" />
              <button class="btn btn--ghost btn--sm upload-clear" @click.stop="clearImage">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
                重新选择
              </button>
            </div>
          </div>
          <div class="upload-actions">
            <button class="btn btn--primary btn--lg" @click="analyzeImage" :disabled="analyzing || !previewImage">
              <svg v-if="analyzing" class="spinner" viewBox="0 0 24 24" width="20" height="20">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="31.416" stroke-dashoffset="10"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
              {{ analyzing ? '识别中...' : '开始识别' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Result Section -->
      <div class="panel">
        <div class="panel-header">
          <h3 class="panel-title">识别结果</h3>
        </div>
        <div class="panel-body">
          <div v-if="result" class="result-content">
            <div class="result-header">
              <div class="result-name">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="24" height="24" style="color: var(--color-danger)">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="8" x2="12" y2="12"/>
                  <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                <span>{{ result.name }}</span>
              </div>
              <div class="result-confidence">
                <span>置信度</span>
                <div class="confidence-bar">
                  <div class="confidence-fill" :style="{ width: `${result.confidence}%` }"></div>
                </div>
                <span>{{ result.confidence }}%</span>
              </div>
            </div>

            <div class="result-section">
              <h4>症状描述</h4>
              <p>{{ result.symptoms }}</p>
            </div>

            <div class="result-section">
              <h4>防治建议</h4>
              <ul>
                <li v-for="(advice, i) in result.advices" :key="i">{{ advice }}</li>
              </ul>
            </div>

            <div class="result-section">
              <h4>推荐用药</h4>
              <div class="drug-tags">
                <span v-for="drug in result.drugs" :key="drug" class="tag tag--warning">{{ drug }}</span>
              </div>
            </div>

            <div class="result-actions">
              <button class="btn btn--primary">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                  <line x1="12" y1="5" x2="12" y2="19"/>
                  <line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
                添加到农事记录
              </button>
              <button class="btn btn--secondary" @click="resetResult">重新识别</button>
            </div>

            <div class="result-other">
              <div class="other-title">其他可能性</div>
              <div v-for="item in result.otherPossibilities" :key="item.name" class="other-item">
                <span>{{ item.name }}</span>
                <div class="mini-bar">
                  <div class="mini-fill" :style="{ width: `${item.confidence}%` }"></div>
                </div>
                <span>{{ item.confidence }}%</span>
              </div>
            </div>
          </div>
          <div v-else class="result-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="64" height="64" style="opacity: 0.3">
              <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/>
              <circle cx="12" cy="13" r="4"/>
            </svg>
            <p>上传图片后开始识别</p>
          </div>
        </div>
      </div>
    </div>

    <!-- History -->
    <div class="panel" style="margin-top: var(--space-lg);">
      <div class="panel-header">
        <h3 class="panel-title">识别历史</h3>
      </div>
      <div class="panel-body">
        <div class="history-grid">
          <div v-for="item in history" :key="item.id" class="history-item">
            <div class="history-image"></div>
            <div class="history-info">
              <div class="history-name">{{ item.name }}</div>
              <div class="history-time">{{ item.time }}</div>
            </div>
            <span :class="['tag', item.confidence > 80 ? 'tag--success' : 'tag--warning']">
              {{ item.confidence }}%
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const fileInput = ref(null)
const previewImage = ref('')
const isDragover = ref(false)
const analyzing = ref(false)
const result = ref(null)

const history = ref([
  { id: 1, name: '稻瘟病', time: '2026-02-14 14:30', confidence: 92 },
  { id: 2, name: '蚜虫', time: '2026-02-13 09:15', confidence: 87 },
  { id: 3, name: '纹枯病', time: '2026-02-12 16:45', confidence: 78 }
])

const triggerUpload = () => fileInput.value?.click()

const handleFileSelect = (e) => {
  const file = e.target.files?.[0]
  if (file) processFile(file)
}

const handleDrop = (e) => {
  isDragover.value = false
  const file = e.dataTransfer.files?.[0]
  if (file && file.type.startsWith('image/')) processFile(file)
}

const processFile = (file) => {
  if (file.size > 5 * 1024 * 1024) return alert('文件大小不能超过5MB')
  previewImage.value = URL.createObjectURL(file)
  result.value = null
}

const clearImage = () => {
  previewImage.value = ''
  result.value = null
}

const analyzeImage = () => {
  if (!previewImage.value || analyzing.value) return
  analyzing.value = true

  setTimeout(() => {
    result.value = {
      name: '稻瘟病',
      confidence: 92,
      symptoms: '叶片出现纺锤形褐色病斑，中央灰白色，边缘褐色。病斑多时汇合成不规则形，严重时叶片枯死。在潮湿条件下，病斑背面产生灰绿色霉层。',
      advices: ['选用抗病品种，合理布局品种', '发病初期及时喷药防治，可选用三环唑、稻瘟灵等', '合理施肥，避免氮肥过量，增施磷钾肥', '田间发现中心病株时，应立即喷药封锁'],
      drugs: ['三环唑', '稻瘟灵', '富士一号', '春雷霉素'],
      otherPossibilities: [{ name: '纹枯病', confidence: 5 }, { name: '褐斑病', confidence: 3 }]
    }
    analyzing.value = false
  }, 2000)
}

const resetResult = () => {
  result.value = null
  previewImage.value = ''
}
</script>

<style lang="scss" scoped>
.upload-zone {
  border: 2px dashed rgba(143, 168, 154, 0.3);
  border-radius: var(--radius-lg);
  padding: var(--space-2xl);
  text-align: center;
  cursor: pointer;
  transition: all var(--duration-normal);

  &:hover, &.upload-zone--dragover {
    border-color: var(--color-emerald);
    background: rgba(46, 204, 113, 0.05);
  }
}

.upload-placeholder {
  color: var(--color-mist);
  svg { margin-bottom: var(--space-md); opacity: 0.5; }
  .upload-text { margin-bottom: var(--space-sm); em { color: var(--color-emerald); font-style: normal; } }
  .upload-hint { font-size: 0.8rem; opacity: 0.6; }
}

.upload-preview {
  position: relative;
  img { max-width: 100%; max-height: 280px; border-radius: var(--radius-md); }
  .upload-clear { position: absolute; bottom: var(--space-md); left: 50%; transform: translateX(-50%); }
}

.upload-actions { margin-top: var(--space-lg); text-align: center; }

.spinner { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.result-content {
  .result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-lg);
    padding-bottom: var(--space-lg);
    border-bottom: var(--border-subtle);

    .result-name { display: flex; align-items: center; gap: var(--space-sm); font-size: 1.25rem; font-weight: 600; }
    .result-confidence { display: flex; align-items: center; gap: var(--space-sm); font-size: 0.9rem; color: var(--color-mist); }
    .confidence-bar { width: 80px; height: 6px; background: rgba(143, 168, 154, 0.2); border-radius: var(--radius-full); overflow: hidden; }
    .confidence-fill { height: 100%; background: var(--color-emerald); }
  }

  .result-section { margin-bottom: var(--space-lg); h4 { color: var(--color-amber); margin-bottom: var(--space-sm); font-size: 0.9rem; } p, li { color: var(--color-cream-muted); line-height: 1.7; } ul { padding-left: var(--space-lg); } }
  .drug-tags { display: flex; flex-wrap: wrap; gap: var(--space-sm); }
  .result-actions { display: flex; gap: var(--space-md); margin: var(--space-lg) 0; }

  .result-other {
    padding-top: var(--space-lg);
    border-top: var(--border-subtle);
    .other-title { font-size: 0.85rem; color: var(--color-mist); margin-bottom: var(--space-md); }
    .other-item { display: flex; align-items: center; gap: var(--space-md); margin-bottom: var(--space-sm); font-size: 0.9rem; }
    .mini-bar { flex: 1; height: 4px; background: rgba(143, 168, 154, 0.2); border-radius: var(--radius-full); overflow: hidden; }
    .mini-fill { height: 100%; background: var(--color-mist); }
  }
}

.result-empty { text-align: center; padding: var(--space-2xl); color: var(--color-mist); }

.history-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: var(--space-md); }
.history-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  background: rgba(255,255,255,0.02);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background var(--duration-normal);
  &:hover { background: rgba(255,255,255,0.04); }
  .history-image { width: 48px; height: 48px; border-radius: var(--radius-sm); background: var(--surface-elevated); }
  .history-info { flex: 1; .history-name { font-weight: 500; } .history-time { font-size: 0.75rem; color: var(--color-mist); } }
}
</style>
