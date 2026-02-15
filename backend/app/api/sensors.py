from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import random

from ..database import get_db
from ..models.models import Sensor, SensorData, AlertRule
from ..models.schemas import (
    SensorCreate, SensorResponse, SensorDataResponse,
    RealtimeDataResponse, MessageResponse
)

router = APIRouter(prefix="/sensors", tags=["传感器"])

# 传感器类型配置
SENSOR_TYPES = {
    "temperature": {"label": "空气温度", "unit": "°C", "min": 15, "max": 35},
    "humidity": {"label": "空气湿度", "unit": "%", "min": 40, "max": 80},
    "ph": {"label": "土壤pH", "unit": "", "min": 5.5, "max": 7.5},
    "light": {"label": "光照强度", "unit": "Lux", "min": 0, "max": 100000},
    "co2": {"label": "CO2浓度", "unit": "ppm", "min": 300, "max": 1000}
}


@router.get("", response_model=List[SensorResponse])
def get_sensors(db: Session = Depends(get_db)):
    """获取所有传感器列表"""
    sensors = db.query(Sensor).all()
    return sensors


@router.get("/realtime", response_model=List[RealtimeDataResponse])
def get_realtime_data():
    """获取实时传感器数据"""
    data = []
    for sensor_type, config in SENSOR_TYPES.items():
        value = round(random.uniform(config["min"], config["max"]), 1)
        # 模拟偶尔超出范围
        if random.random() < 0.1:
            if random.random() < 0.5:
                value = config["min"] - random.uniform(1, 5)
            else:
                value = config["max"] + random.uniform(1, 5)

        is_warning = value < config["min"] or value > config["max"]

        data.append(RealtimeDataResponse(
            type=sensor_type,
            label=config["label"],
            value=round(value, 1),
            unit=config["unit"],
            min=config["min"],
            max=config["max"],
            is_warning=is_warning
        ))
    return data


@router.get("/history")
def get_history_data(
    sensor_type: str = "temperature",
    time_range: str = "24h",
    db: Session = Depends(get_db)
):
    """获取历史数据"""
    # 生成模拟历史数据
    now = datetime.utcnow()

    if time_range == "24h":
        points = 24
        delta = timedelta(hours=1)
    elif time_range == "7d":
        points = 7
        delta = timedelta(days=1)
    else:
        points = 30
        delta = timedelta(days=1)

    config = SENSOR_TYPES.get(sensor_type, SENSOR_TYPES["temperature"])

    data = []
    for i in range(points):
        timestamp = now - delta * (points - i - 1)
        base_value = (config["min"] + config["max"]) / 2
        variation = (config["max"] - config["min"]) * 0.3
        value = base_value + random.uniform(-variation, variation)

        data.append({
            "timestamp": timestamp.isoformat(),
            "value": round(value, 2)
        })

    return {"sensor_type": sensor_type, "time_range": time_range, "data": data}


@router.post("", response_model=SensorResponse)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    """创建新传感器"""
    # 生成传感器ID
    count = db.query(Sensor).count()
    sensor_id = f"S{str(count + 1).zfill(3)}"

    config = SENSOR_TYPES.get(sensor.type, {})

    db_sensor = Sensor(
        name=sensor.name,
        sensor_id=sensor_id,
        type=sensor.type,
        location=sensor.location,
        unit=sensor.unit or config.get("unit", ""),
        min_value=sensor.min_value or config.get("min"),
        max_value=sensor.max_value or config.get("max"),
        status="online"
    )
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


@router.delete("/{sensor_id}", response_model=MessageResponse)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    """删除传感器"""
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="传感器不存在")

    db.delete(sensor)
    db.commit()
    return MessageResponse(message="删除成功")
