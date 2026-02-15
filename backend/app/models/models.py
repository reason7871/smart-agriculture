from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sensor_id = Column(String(50), unique=True, index=True)
    type = Column(String(50))  # temperature, humidity, ph, light, co2
    location = Column(String(100))
    unit = Column(String(20))
    min_value = Column(Float)
    max_value = Column(Float)
    status = Column(String(20), default="online")  # online, offline
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    data_records = relationship("SensorData", back_populates="sensor")


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    value = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    sensor = relationship("Sensor", back_populates="data_records")


class Plot(Base):
    __tablename__ = "plots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    area = Column(Float)  # 面积(亩)
    location = Column(String(100))
    soil_type = Column(String(50))
    status = Column(String(20), default="空闲")  # 空闲, 种植中
    created_at = Column(DateTime, default=datetime.utcnow)

    crops = relationship("CropRecord", back_populates="plot")


class CropRecord(Base):
    __tablename__ = "crop_records"

    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(Integer, ForeignKey("plots.id"))
    crop_name = Column(String(100))
    variety = Column(String(100))
    planting_date = Column(DateTime)
    expected_harvest = Column(DateTime)
    growth_stage = Column(String(50))
    status = Column(String(20), default="种植中")
    progress = Column(Integer, default=0)  # 生长进度百分比
    created_at = Column(DateTime, default=datetime.utcnow)

    plot = relationship("Plot", back_populates="crops")
    tasks = relationship("FarmTask", back_populates="crop_record")


class FarmTask(Base):
    __tablename__ = "farm_tasks"

    id = Column(Integer, primary_key=True, index=True)
    crop_record_id = Column(Integer, ForeignKey("crop_records.id"))
    task_type = Column(String(50))  # 播种, 施肥, 浇水, 除草, 喷药, 收获
    scheduled_date = Column(DateTime)
    completed_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="pending")  # pending, completed
    description = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    crop_record = relationship("CropRecord", back_populates="tasks")


class DiseaseRecord(Base):
    __tablename__ = "disease_records"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String(255))
    disease_name = Column(String(100))
    confidence = Column(Float)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sensor_type = Column(String(50))
    condition = Column(String(50))  # gt, lt, gte, lte
    threshold = Column(Float)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
