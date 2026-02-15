# 智慧农业管理系统

一个现代化的智慧农业 Web 应用，采用生态未来主义设计风格，集成机器学习的产量预测功能。

![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

## 功能模块

### 控制中心
- 实时环境数据展示
- 农事任务时间线
- 系统告警通知
- 天气信息展示

### 环境监测
- 传感器数据实时监控
- 历史数据趋势图表
- 告警规则配置
- 传感器管理（增删改查）

### 作物管理
- 地块信息管理
- 农事记录跟踪
- 生长阶段时间线
- 任务计划与完成状态

### 病虫害识别
- 图片拖拽上传
- AI 病虫害识别（模拟）
- 诊断结果与防治建议
- 推荐用药方案
- 识别历史记录

### 数据分析
- 产量趋势分析
- 作物产量占比
- **产量预测**（集成机器学习模型）
- 详细数据报表

### 系统设置
- 基本信息配置
- 通知偏好设置
- 告警阈值配置
- 数据导入导出

## 产量预测算法

系统采用**集成预测模型 (Ensemble Forecasting)**，组合多种算法提高预测准确性：

| 预测器 | 权重 | 说明 |
|--------|------|------|
| 移动平均预测器 | 15% | 基于近期数据算术平均 |
| 指数平滑预测器 | 30% | 近期数据权重更高，捕捉趋势 |
| 季节性预测器 | 35% | 识别农业生产季节性规律 |
| 多因素预测器 | 20% | 综合温度、降雨、施肥等因素 |

考虑因素：温度、降雨量、施肥量、土壤pH、日照时长

## 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Vue Router** - 官方路由管理器
- **Pinia** - 状态管理
- **ECharts** - 数据可视化
- **SCSS** - CSS 预处理器
- **Axios** - HTTP 客户端

### 后端
- **FastAPI** - 高性能 Python Web 框架
- **SQLAlchemy** - ORM 工具
- **Pydantic** - 数据验证
- **NumPy** - 数值计算
- **SQLite** - 开发数据库

## 项目结构

```
nongye/
├── frontend/                # 前端项目
│   ├── src/
│   │   ├── api/            # API 接口
│   │   ├── layouts/        # 布局组件
│   │   ├── router/         # 路由配置
│   │   ├── stores/         # 状态管理
│   │   ├── styles/         # 样式文件
│   │   └── views/          # 页面组件
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务服务（含预测算法）
│   │   ├── config.py       # 配置
│   │   └── database.py     # 数据库
│   ├── main.py             # 应用入口
│   └── requirements.txt    # Python 依赖
│
└── README.md
```

## 快速开始

### 环境要求
- Node.js 18+
- Python 3.10+
- npm 或 yarn

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

后端服务将运行在 http://localhost:8000

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将运行在 http://localhost:5173

## API 文档

启动后端后，访问以下地址查看 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/sensors` | GET/POST | 传感器列表/创建 |
| `/api/sensors/{id}/data` | GET | 传感器历史数据 |
| `/api/plots` | GET/POST | 地块列表/创建 |
| `/api/disease/analyze` | POST | 病虫害识别 |
| `/api/forecast/predict` | GET | 产量预测 |
| `/api/forecast/algorithm/info` | GET | 预测算法说明 |

## 设计特点

- **生态未来主义风格** - 深绿色为主色调，金色强调
- **有机曲线设计** - 模拟植物叶脉纹理的背景
- **数据可视化动画** - 图表数据"生长"效果
- **响应式布局** - 适配不同屏幕尺寸

## License

MIT License
