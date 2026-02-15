import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '首页概览', icon: 'HomeFilled' }
      },
      {
        path: 'monitor',
        name: 'Monitor',
        component: () => import('@/views/Monitor.vue'),
        meta: { title: '环境监测', icon: 'DataLine' }
      },
      {
        path: 'crops',
        name: 'Crops',
        component: () => import('@/views/Crops.vue'),
        meta: { title: '作物管理', icon: 'Grid' }
      },
      {
        path: 'disease',
        name: 'Disease',
        component: () => import('@/views/Disease.vue'),
        meta: { title: '病虫害识别', icon: 'Camera' }
      },
      {
        path: 'analysis',
        name: 'Analysis',
        component: () => import('@/views/Analysis.vue'),
        meta: { title: '数据分析', icon: 'TrendCharts' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/Settings.vue'),
        meta: { title: '系统设置', icon: 'Setting' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
