"""
产量预测 API 路由
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from ..services.forecast import forecast_service, generate_mock_historical_data

router = APIRouter(prefix="/forecast", tags=["产量预测"])


class EnvironmentFactors(BaseModel):
    """环境因素模型"""
    temperature: Optional[float] = 25.0      # 温度 (°C)
    rainfall: Optional[float] = 150.0        # 降雨量 (mm)
    fertilizer: Optional[float] = 50.0       # 施肥量 (kg/亩)
    soil_ph: Optional[float] = 6.5           # 土壤pH
    sunshine: Optional[float] = 8.0          # 日照时长 (小时)


class ForecastRequest(BaseModel):
    """预测请求模型"""
    crop: str = "水稻"
    periods: int = 3
    factors: Optional[EnvironmentFactors] = None


@router.get("/predict")
async def predict_yield(
    crop: str = Query("水稻", description="作物类型: 水稻, 玉米, 蔬菜, 小麦"),
    periods: int = Query(3, description="预测期数(月)", ge=1, le=12)
):
    """
    产量预测接口

    返回指定作物未来几个月的产量预测结果，包括：
    - 各期预测值
    - 置信区间
    - 趋势判断
    - 算法信息
    """
    valid_crops = ['水稻', '玉米', '蔬菜', '小麦']
    if crop not in valid_crops:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的作物类型: {crop}。支持的作物: {', '.join(valid_crops)}"
        )

    try:
        result = forecast_service.forecast(crop=crop, periods=periods)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预测失败: {str(e)}")


@router.post("/predict")
async def predict_with_factors(request: ForecastRequest):
    """
    带环境因素的产量预测

    根据当前环境因素进行更精准的产量预测
    """
    valid_crops = ['水稻', '玉米', '蔬菜', '小麦']
    if request.crop not in valid_crops:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的作物类型: {request.crop}"
        )

    try:
        factors_dict = None
        if request.factors:
            factors_dict = request.factors.dict()

        result = forecast_service.forecast(
            crop=request.crop,
            periods=request.periods,
            current_factors=factors_dict
        )
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预测失败: {str(e)}")


@router.get("/history/{crop}")
async def get_historical_data(crop: str):
    """
    获取历史产量数据
    """
    all_data = generate_mock_historical_data(24)
    crop_data = [d for d in all_data if d.get('crop') == crop]

    if not crop_data:
        raise HTTPException(status_code=404, detail=f"未找到作物 {crop} 的历史数据")

    return {
        "success": True,
        "data": crop_data
    }


@router.get("/compare")
async def compare_crops(
    crops: str = Query("水稻,玉米,蔬菜", description="要比较的作物，逗号分隔"),
    periods: int = Query(3, description="预测期数")
):
    """
    多作物产量预测对比

    同时预测多种作物的产量，用于对比分析
    """
    crop_list = [c.strip() for c in crops.split(',')]
    valid_crops = ['水稻', '玉米', '蔬菜', '小麦']

    invalid = [c for c in crop_list if c not in valid_crops]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的作物: {', '.join(invalid)}"
        )

    results = {}
    for crop in crop_list:
        try:
            results[crop] = forecast_service.forecast(crop=crop, periods=periods)
        except Exception as e:
            results[crop] = {"error": str(e)}

    return {
        "success": True,
        "data": results
    }


@router.get("/algorithm/info")
async def get_algorithm_info():
    """
    获取预测算法信息

    返回当前使用的预测算法详情
    """
    return {
        "success": True,
        "data": {
            "name": "集成预测模型 (Ensemble Forecasting)",
            "version": "1.0.0",
            "description": "组合多种预测算法提高准确性",
            "components": [
                {
                    "name": "移动平均预测器",
                    "type": "MovingAveragePredictor",
                    "weight": 0.15,
                    "description": "基于近期数据的算术平均，适用于短期预测"
                },
                {
                    "name": "指数平滑预测器",
                    "type": "ExponentialSmoothingPredictor",
                    "weight": 0.30,
                    "description": "对近期数据赋予更高权重，捕捉趋势变化"
                },
                {
                    "name": "季节性预测器",
                    "type": "SeasonalPredictor",
                    "weight": 0.35,
                    "description": "识别并利用农业生产的季节性规律"
                },
                {
                    "name": "多因素预测器",
                    "type": "MultiFactorPredictor",
                    "weight": 0.20,
                    "description": "综合考虑温度、降雨、施肥等环境因素"
                }
            ],
            "factors_considered": [
                {"name": "temperature", "description": "环境温度", "optimal_range": "20-30°C"},
                {"name": "rainfall", "description": "月降雨量", "optimal_range": "100-200mm"},
                {"name": "fertilizer", "description": "施肥量", "unit": "kg/亩"},
                {"name": "soil_ph", "description": "土壤酸碱度", "optimal_range": "6.0-7.0"},
                {"name": "sunshine", "description": "日照时长", "unit": "小时/天"}
            ],
            "confidence_level": 0.85,
            "accuracy_note": "预测准确性取决于历史数据质量和环境因素的稳定性"
        }
    }
