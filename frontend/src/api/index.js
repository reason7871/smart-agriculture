import request from './request'

// 传感器相关API
export const sensorApi = {
  getList: () => request.get('/sensors'),
  getDetail: (id) => request.get(`/sensors/${id}`),
  create: (data) => request.post('/sensors', data),
  update: (id, data) => request.put(`/sensors/${id}`, data),
  delete: (id) => request.delete(`/sensors/${id}`),
  getRealtimeData: () => request.get('/sensors/realtime'),
  getHistoryData: (params) => request.get('/sensors/history', { params })
}

// 地块相关API
export const plotApi = {
  getList: () => request.get('/plots'),
  getDetail: (id) => request.get(`/plots/${id}`),
  create: (data) => request.post('/plots', data),
  update: (id, data) => request.put(`/plots/${id}`, data),
  delete: (id) => request.delete(`/plots/${id}`)
}

// 农事任务相关API
export const taskApi = {
  getList: (plotId) => request.get('/tasks', { params: { plotId } }),
  create: (data) => request.post('/tasks', data),
  update: (id, data) => request.put(`/tasks/${id}`, data),
  complete: (id) => request.put(`/tasks/${id}/complete`),
  delete: (id) => request.delete(`/tasks/${id}`)
}

// 病虫害识别相关API
export const diseaseApi = {
  analyze: (formData) => request.post('/disease/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getHistory: () => request.get('/disease/history')
}

// 数据分析相关API
export const analysisApi = {
  getProduction: (params) => request.get('/analysis/production', { params }),
  getYieldForecast: (params) => request.get('/analysis/forecast', { params }),
  getCorrelation: (params) => request.get('/analysis/correlation', { params })
}

export default {
  sensorApi,
  plotApi,
  taskApi,
  diseaseApi,
  analysisApi
}
