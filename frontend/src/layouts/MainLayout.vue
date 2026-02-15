<template>
  <div class="app-layout">
    <!-- Living Background -->
    <div class="app-background"></div>
    <div class="ambient-glow ambient-glow--amber"></div>
    <div class="ambient-glow ambient-glow--emerald"></div>

    <!-- Sidebar - Tree Trunk -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L12 6M12 18L12 22M6 12L2 12M22 12L18 12"/>
            <path d="M12 12C12 12 8 8 8 12C8 16 12 12 12 12C12 12 16 8 16 12C16 16 12 12 12 12"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
        </div>
        <div>
          <div class="logo-text">智慧农业</div>
          <div class="logo-tagline">Eco Intelligence</div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section">
          <div class="nav-section-title">核心功能</div>
          <router-link
            v-for="item in mainNavItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <component :is="item.icon" class="nav-icon" />
            <span class="nav-label">{{ item.label }}</span>
            <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
          </router-link>
        </div>

        <div class="nav-section">
          <div class="nav-section-title">系统</div>
          <router-link
            v-for="item in systemNavItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <component :is="item.icon" class="nav-icon" />
            <span class="nav-label">{{ item.label }}</span>
          </router-link>
        </div>
      </nav>

      <!-- Sidebar Footer -->
      <div class="sidebar-footer">
        <div class="weather-widget">
          <div class="weather-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="4"/>
              <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
            </svg>
          </div>
          <div class="weather-info">
            <div class="weather-temp">26°C</div>
            <div class="weather-desc">晴朗 · 适宜农事</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Header -->
      <header class="content-header">
        <div class="header-left">
          <h1 class="page-title">{{ pageTitle }}</h1>
          <div class="header-time">
            <span class="live-indicator"></span>
            {{ currentTime }}
          </div>
        </div>
        <div class="header-right">
          <button class="btn btn--ghost btn--sm" @click="refreshData">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
              <path d="M21 12a9 9 0 11-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/>
              <path d="M21 3v5h-5"/>
            </svg>
            刷新
          </button>
          <button class="btn btn--ghost btn--sm">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
              <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 01-3.46 0"/>
            </svg>
            <span class="alert-badge" v-if="alertCount > 0">{{ alertCount }}</span>
          </button>
          <div class="user-menu">
            <div class="user-avatar">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="8" r="4"/>
                <path d="M20 21a8 8 0 10-16 0"/>
              </svg>
            </div>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <div class="content-view">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, markRaw } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentTime = ref('')
const alertCount = ref(3)

// Icon components as raw SVG wrappers
const HomeIcon = markRaw({
  template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`
})

const ChartIcon = markRaw({
  template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`
})

const GridIcon = markRaw({
  template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>`
})

const CameraIcon = markRaw({
  template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/><circle cx="12" cy="13" r="4"/></svg>`
})

const TrendIcon = markRaw({
  template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>`
})

const SettingsIcon = markRaw({
  template: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>`
})

const mainNavItems = [
  { path: '/dashboard', label: '控制中心', icon: HomeIcon },
  { path: '/monitor', label: '环境监测', icon: ChartIcon },
  { path: '/crops', label: '作物管理', icon: GridIcon },
  { path: '/disease', label: '病虫害识别', icon: CameraIcon, badge: 2 },
  { path: '/analysis', label: '数据分析', icon: TrendIcon }
]

const systemNavItems = [
  { path: '/settings', label: '系统设置', icon: SettingsIcon }
]

const pageTitle = computed(() => {
  const titles = {
    '/dashboard': '控制中心',
    '/monitor': '环境监测',
    '/crops': '作物管理',
    '/disease': '病虫害识别',
    '/analysis': '数据分析',
    '/settings': '系统设置'
  }
  return titles[route.path] || '智慧农业'
})

const isActive = (path) => {
  return route.path === path
}

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const refreshData = () => {
  window.location.reload()
}

let timer = null

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 60000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style lang="scss" scoped>
.sidebar-footer {
  padding: var(--space-lg);
  border-top: var(--border-subtle);
}

.weather-widget {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  background: var(--surface-glass);
  border-radius: var(--radius-md);

  .weather-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-amber);

    svg {
      width: 28px;
      height: 28px;
    }
  }

  .weather-info {
    .weather-temp {
      font-family: var(--font-display);
      font-size: 1.25rem;
      font-weight: 600;
      color: var(--color-cream);
    }

    .weather-desc {
      font-size: 0.75rem;
      color: var(--color-mist);
    }
  }
}

.user-menu {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: var(--surface-elevated);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-mist);
  cursor: pointer;
  transition: all var(--duration-normal);

  &:hover {
    background: var(--color-fern);
    color: var(--color-cream);
  }

  svg {
    width: 18px;
    height: 18px;
  }
}

.alert-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background: var(--color-danger);
  color: white;
  font-size: 0.65rem;
  font-weight: 600;
  min-width: 16px;
  height: 16px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
}

// Page transition
.page-enter-active,
.page-leave-active {
  transition: all 0.3s var(--ease-natural);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
