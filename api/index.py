"""
Vercel Serverless Function Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI(
    title="智慧农业管理系统",
    version="1.0.0",
    description="智慧农业管理系统后端API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for sensors
MOCK_SENSORS = [
    {"id": 1, "name": "温度传感器-A1", "type": "temperature", "location": "地块A", "value": 25.5, "unit": "°C", "status": "online"},
    {"id": 2, "name": "湿度传感器-A2", "type": "humidity", "location": "地块A", "value": 68.2, "unit": "%", "status": "online"},
    {"id": 3, "name": "土壤pH传感器-B1", "type": "ph", "location": "地块B", "value": 6.8, "unit": "pH", "status": "online"},
]

MOCK_PLOTS = [
    {"id": 1, "name": "地块A", "area": 5, "crop": "水稻", "status": "种植中", "progress": 65},
    {"id": 2, "name": "地块B", "area": 3, "crop": "玉米", "status": "种植中", "progress": 40},
    {"id": 3, "name": "温室1", "area": 1, "crop": "番茄", "status": "种植中", "progress": 75},
]

# Routes
@app.get("/")
def root():
    return {"message": "智慧农业管理系统 API", "version": "1.0.0"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/sensors")
def get_sensors():
    return {"success": True, "data": MOCK_SENSORS}


@app.get("/api/sensors/{sensor_id}")
def get_sensor(sensor_id: int):
    for sensor in MOCK_SENSORS:
        if sensor["id"] == sensor_id:
            return {"success": True, "data": sensor}
    return {"success": False, "message": "传感器不存在"}


@app.get("/api/sensors/{sensor_id}/data")
def get_sensor_data(sensor_id: int):
    import random
    data = []
    for i in range(24):
        data.append({
            "time": f"{i:02d}:00",
            "value": round(random.uniform(20, 30), 1)
        })
    return {"success": True, "data": data}


@app.post("/api/sensors")
def create_sensor(data: dict):
    return {"success": True, "message": "传感器创建成功", "data": data}


@app.get("/api/plots")
def get_plots():
    return {"success": True, "data": MOCK_PLOTS}


@app.get("/api/plots/{plot_id}")
def get_plot(plot_id: int):
    for plot in MOCK_PLOTS:
        if plot["id"] == plot_id:
            return {"success": True, "data": plot}
    return {"success": False, "message": "地块不存在"}


@app.get("/api/analysis/summary")
def get_analysis_summary():
    return {
        "success": True,
        "data": {
            "total_yield": 12500,
            "avg_yield_per_acre": 2500,
            "total_cost": 8500,
            "expected_revenue": 32000
        }
    }


@app.get("/api/analysis/trends")
def get_analysis_trends():
    return {
        "success": True,
        "data": {
            "labels": ["1月", "2月", "3月", "4月", "5月", "6月"],
            "rice": [0, 0, 1200, 1500, 1800, 2000],
            "corn": [0, 0, 0, 0, 800, 1200],
            "vegetables": [500, 600, 700, 800, 900, 600]
        }
    }


@app.post("/api/disease/analyze")
def analyze_disease(data: dict):
    return {
        "success": True,
        "data": {
            "name": "稻瘟病",
            "confidence": 92,
            "symptoms": "叶片出现纺锤形褐色病斑，中央灰白色，边缘褐色。",
            "advices": [
                "选用抗病品种，合理布局品种",
                "发病初期及时喷药防治",
                "合理施肥，避免氮肥过量"
            ],
            "drugs": ["三环唑", "稻瘟灵", "富士一号"]
        }
    }


@app.get("/api/forecast/predict")
def forecast_predict(crop: str = "水稻", periods: int = 3):
    import math

    predictions = []
    base_yield = {"水稻": 2200, "玉米": 1800, "蔬菜": 800, "小麦": 1500}.get(crop, 2000)

    for i in range(1, periods + 1):
        predicted = base_yield * (1 + 0.05 * i)
        margin = predicted * 0.1
        predictions.append({
            "period": i,
            "predicted_yield": round(predicted, 0),
            "confidence_lower": round(predicted - margin, 0),
            "confidence_upper": round(predicted + margin, 0),
            "confidence_level": 0.85,
            "trend": "up"
        })

    total = sum(p["predicted_yield"] for p in predictions)

    return {
        "success": True,
        "data": {
            "crop": crop,
            "forecast_periods": periods,
            "predictions": predictions,
            "summary": {
                "total_predicted_yield": round(total, 0),
                "average_monthly_yield": round(total / periods, 0),
                "overall_confidence": 0.85,
                "prediction_range": [round(total * 0.9, 0), round(total * 1.1, 0)]
            }
        }
    }


@app.get("/api/forecast/algorithm/info")
def forecast_algorithm_info():
    return {
        "success": True,
        "data": {
            "name": "集成预测模型",
            "version": "1.0.0",
            "description": "组合多种预测算法提高准确性",
            "components": [
                {"name": "移动平均预测器", "weight": 0.15, "description": "基于近期数据的算术平均"},
                {"name": "指数平滑预测器", "weight": 0.30, "description": "对近期数据赋予更高权重"},
                {"name": "季节性预测器", "weight": 0.35, "description": "识别农业生产季节性规律"},
                {"name": "多因素预测器", "weight": 0.20, "description": "综合环境因素预测"}
            ],
            "factors_considered": [
                {"name": "temperature", "description": "环境温度", "optimal_range": "20-30°C"},
                {"name": "rainfall", "description": "月降雨量", "optimal_range": "100-200mm"},
                {"name": "fertilizer", "description": "施肥量"},
                {"name": "soil_ph", "description": "土壤酸碱度", "optimal_range": "6.0-7.0"},
                {"name": "sunshine", "description": "日照时长"}
            ]
        }
    }


# Vercel handler (using Mangum for ASGI support)
handler = Mangum(app)
