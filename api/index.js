// Vercel Serverless Function - Node.js
export default function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const { method } = req;
  const path = req.url.split('?')[0];

  // Mock data
  const mockSensors = [
    { id: 1, name: '温度传感器-A1', type: 'temperature', location: '地块A', value: 25.5, unit: '°C', status: 'online' },
    { id: 2, name: '湿度传感器-A2', type: 'humidity', location: '地块A', value: 68.2, unit: '%', status: 'online' },
    { id: 3, name: '土壤pH传感器-B1', type: 'ph', location: '地块B', value: 6.8, unit: 'pH', status: 'online' },
  ];

  const mockPlots = [
    { id: 1, name: '地块A', area: 5, crop: '水稻', status: '种植中', progress: 65 },
    { id: 2, name: '地块B', area: 3, crop: '玉米', status: '种植中', progress: 40 },
    { id: 3, name: '温室1', area: 1, crop: '番茄', status: '种植中', progress: 75 },
  ];

  // Routing
  if (path === '/' || path === '') {
    return res.json({ message: '智慧农业管理系统 API', version: '1.0.0' });
  }

  if (path === '/api/health') {
    return res.json({ status: 'healthy' });
  }

  if (path === '/api/sensors') {
    return res.json({ success: true, data: mockSensors });
  }

  if (path === '/api/plots') {
    return res.json({ success: true, data: mockPlots });
  }

  if (path === '/api/analysis/summary') {
    return res.json({
      success: true,
      data: {
        total_yield: 12500,
        avg_yield_per_acre: 2500,
        total_cost: 8500,
        expected_revenue: 32000
      }
    });
  }

  if (path === '/api/analysis/trends') {
    return res.json({
      success: true,
      data: {
        labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
        rice: [0, 0, 1200, 1500, 1800, 2000],
        corn: [0, 0, 0, 0, 800, 1200],
        vegetables: [500, 600, 700, 800, 900, 600]
      }
    });
  }

  if (path === '/api/disease/analyze' && method === 'POST') {
    return res.json({
      success: true,
      data: {
        name: '稻瘟病',
        confidence: 92,
        symptoms: '叶片出现纺锤形褐色病斑，中央灰白色，边缘褐色。',
        advices: ['选用抗病品种', '发病初期及时喷药防治', '合理施肥'],
        drugs: ['三环唑', '稻瘟灵', '富士一号']
      }
    });
  }

  if (path === '/api/forecast/predict') {
    const { crop = '水稻', periods = 3 } = req.query;
    const baseYield = { '水稻': 2200, '玉米': 1800, '蔬菜': 800, '小麦': 1500 }[crop] || 2000;
    const p = parseInt(periods);

    const predictions = [];
    for (let i = 1; i <= p; i++) {
      const predicted = baseYield * (1 + 0.05 * i);
      predictions.push({
        period: i,
        predicted_yield: Math.round(predicted),
        confidence_lower: Math.round(predicted * 0.9),
        confidence_upper: Math.round(predicted * 1.1),
        confidence_level: 0.85,
        trend: 'up'
      });
    }

    const total = predictions.reduce((sum, p) => sum + p.predicted_yield, 0);

    return res.json({
      success: true,
      data: {
        crop,
        forecast_periods: p,
        predictions,
        summary: {
          total_predicted_yield: Math.round(total),
          average_monthly_yield: Math.round(total / p),
          overall_confidence: 0.85,
          prediction_range: [Math.round(total * 0.9), Math.round(total * 1.1)]
        }
      }
    });
  }

  if (path === '/api/forecast/algorithm/info') {
    return res.json({
      success: true,
      data: {
        name: '集成预测模型',
        version: '1.0.0',
        description: '组合多种预测算法提高准确性',
        components: [
          { name: '移动平均预测器', weight: 0.15, description: '基于近期数据的算术平均' },
          { name: '指数平滑预测器', weight: 0.30, description: '对近期数据赋予更高权重' },
          { name: '季节性预测器', weight: 0.35, description: '识别农业生产季节性规律' },
          { name: '多因素预测器', weight: 0.20, description: '综合环境因素预测' }
        ],
        factors_considered: [
          { name: 'temperature', description: '环境温度', optimal_range: '20-30°C' },
          { name: 'rainfall', description: '月降雨量', optimal_range: '100-200mm' },
          { name: 'fertilizer', description: '施肥量' },
          { name: 'soil_ph', description: '土壤酸碱度', optimal_range: '6.0-7.0' },
          { name: 'sunshine', description: '日照时长' }
        ]
      }
    });
  }

  // 404 for unmatched routes
  res.status(404).json({ success: false, message: 'Not found' });
}
