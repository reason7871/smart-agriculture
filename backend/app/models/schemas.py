from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ============ 传感器相关 ============
class SensorBase(BaseModel):
    name: str
    type: str
    location: str
    unit: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None

class SensorCreate(SensorBase):
    pass

class SensorResponse(SensorBase):
    id: int
    sensor_id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class SensorDataResponse(BaseModel):
    id: int
    sensor_id: int
    value: float
    recorded_at: datetime

    class Config:
        from_attributes = True

class RealtimeDataResponse(BaseModel):
    type: str
    label: str
    value: float
    unit: str
    min: float
    max: float
    is_warning: bool

# ============ 地块相关 ============
class PlotBase(BaseModel):
    name: str
    area: float
    location: Optional[str] = None
    soil_type: Optional[str] = None

class PlotCreate(PlotBase):
    pass

class PlotResponse(PlotBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# ============ 作物记录相关 ============
class CropRecordBase(BaseModel):
    crop_name: str
    variety: Optional[str] = None
    planting_date: datetime
    expected_harvest: Optional[datetime] = None

class CropRecordCreate(CropRecordBase):
    plot_id: int

class CropRecordResponse(CropRecordBase):
    id: int
    plot_id: int
    growth_stage: Optional[str]
    status: str
    progress: int
    created_at: datetime

    class Config:
        from_attributes = True

# ============ 农事任务相关 ============
class FarmTaskBase(BaseModel):
    task_type: str
    scheduled_date: datetime
    description: Optional[str] = None

class FarmTaskCreate(FarmTaskBase):
    crop_record_id: int

class FarmTaskResponse(FarmTaskBase):
    id: int
    crop_record_id: int
    status: str
    completed_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

# ============ 病虫害识别相关 ============
class DiseaseAnalyzeResponse(BaseModel):
    name: str
    confidence: float
    symptoms: str
    advices: List[str]
    drugs: List[str]
    other_possibilities: List[dict]

class DiseaseHistoryResponse(BaseModel):
    id: int
    image_path: str
    disease_name: str
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True

# ============ 数据分析相关 ============
class ProductionData(BaseModel):
    period: str
    crop: str
    area: float
    production: float
    yield_per_acre: float
    cost: float
    revenue: float
    profit: float

class ForecastResponse(BaseModel):
    predicted_yield: float
    confidence_interval: List[float]
    confidence_level: float

# ============ 通用响应 ============
class MessageResponse(BaseModel):
    message: str
    success: bool = True
