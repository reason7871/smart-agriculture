from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import random

from ..database import get_db
from ..models.schemas import ProductionData, ForecastResponse

router = APIRouter(prefix="/analysis", tags=["数据分析"])


@router.get("/production", response_model=List[ProductionData])
def get_production_data(
    time_range: str = Query("month", regex="^(month|quarter|year)$"),
    plot_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取产量数据"""

    # 模拟数据
    if time_range == "month":
        periods = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    elif time_range == "quarter":
        periods = ["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1"]
    else:
        periods = ["2023年", "2024年", "2025年", "2026年"]

    crops = ["水稻", "玉米", "蔬菜"]

    data = []
    for period in periods:
        for crop in crops:
            area = round(random.uniform(2, 8), 1)
            yield_per_acre = random.randint(1500, 3000)
            production = round(area * yield_per_acre)
            cost = round(production * random.uniform(0.2, 0.4))
            revenue = round(production * random.uniform(1.0, 2.0))
            profit = revenue - cost

            data.append(ProductionData(
                period=period,
                crop=crop,
                area=area,
                production=production,
                yield_per_acre=yield_per_acre,
                cost=cost,
                revenue=revenue,
                profit=profit
            ))

    return data


@router.get("/forecast", response_model=ForecastResponse)
def get_yield_forecast(
    plot_id: Optional[int] = None,
    crop_type: str = "水稻",
    db: Session = Depends(get_db)
):
    """获取产量预测"""

    # 模拟预测结果
    base_yield = random.randint(2000, 3000)
    variation = random.randint(100, 300)

    return ForecastResponse(
        predicted_yield=base_yield,
        confidence_interval=[base_yield - variation, base_yield + variation],
        confidence_level=random.uniform(0.8, 0.95)
    )


@router.get("/correlation")
def get_correlation_analysis(
    factor1: str = "temperature",
    factor2: str = "yield",
    db: Session = Depends(get_db)
):
    """获取关联分析"""

    # 模拟相关系数
    correlation = random.uniform(-0.8, 0.9)

    # 生成散点数据
    scatter_data = []
    for _ in range(50):
        x = random.uniform(15, 35)
        # 根据相关系数生成y值
        y = 1500 + correlation * (x - 25) * 50 + random.uniform(-200, 200)
        scatter_data.append([round(x, 1), round(max(500, y), 0)])

    return {
        "factor1": factor1,
        "factor2": factor2,
        "correlation": round(correlation, 2),
        "scatter_data": scatter_data,
        "interpretation": "强正相关" if correlation > 0.6 else "弱正相关" if correlation > 0 else "负相关"
    }


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    """获取总览数据"""

    return {
        "total_plots": random.randint(8, 15),
        "total_area": random.randint(100, 200),
        "total_sensors": random.randint(30, 60),
        "monthly_production": random.randint(2000, 4000),
        "production_trend": random.uniform(-0.1, 0.2),
        "alerts_count": random.randint(0, 5)
    }
