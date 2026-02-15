from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.models import Plot, CropRecord, FarmTask
from ..models.schemas import (
    PlotCreate, PlotResponse, CropRecordCreate,
    CropRecordResponse, FarmTaskCreate, FarmTaskResponse,
    MessageResponse
)

router = APIRouter(prefix="/plots", tags=["地块管理"])


@router.get("", response_model=List[PlotResponse])
def get_plots(db: Session = Depends(get_db)):
    """获取所有地块"""
    plots = db.query(Plot).all()

    # 添加额外信息
    result = []
    for plot in plots:
        plot_dict = {
            "id": plot.id,
            "name": plot.name,
            "area": plot.area,
            "location": plot.location,
            "soil_type": plot.soil_type,
            "status": plot.status,
            "created_at": plot.created_at
        }
        result.append(plot_dict)

    return result


@router.post("", response_model=PlotResponse)
def create_plot(plot: PlotCreate, db: Session = Depends(get_db)):
    """创建新地块"""
    db_plot = Plot(
        name=plot.name,
        area=plot.area,
        location=plot.location,
        soil_type=plot.soil_type,
        status="空闲"
    )
    db.add(db_plot)
    db.commit()
    db.refresh(db_plot)
    return db_plot


@router.get("/{plot_id}")
def get_plot_detail(plot_id: int, db: Session = Depends(get_db)):
    """获取地块详情"""
    plot = db.query(Plot).filter(Plot.id == plot_id).first()
    if not plot:
        raise HTTPException(status_code=404, detail="地块不存在")

    # 获取当前作物
    current_crop = db.query(CropRecord).filter(
        CropRecord.plot_id == plot_id,
        CropRecord.status == "种植中"
    ).first()

    return {
        **plot.__dict__,
        "current_crop": current_crop
    }


@router.delete("/{plot_id}", response_model=MessageResponse)
def delete_plot(plot_id: int, db: Session = Depends(get_db)):
    """删除地块"""
    plot = db.query(Plot).filter(Plot.id == plot_id).first()
    if not plot:
        raise HTTPException(status_code=404, detail="地块不存在")

    db.delete(plot)
    db.commit()
    return MessageResponse(message="删除成功")


# ============ 农事任务相关 ============

@router.get("/tasks/all")
def get_all_tasks(plot_id: int = None, db: Session = Depends(get_db)):
    """获取所有农事任务"""
    query = db.query(FarmTask)

    if plot_id:
        # 通过CropRecord关联查询
        query = query.join(CropRecord).filter(CropRecord.plot_id == plot_id)

    tasks = query.order_by(FarmTask.scheduled_date.desc()).all()

    result = []
    for task in tasks:
        crop_record = db.query(CropRecord).filter(CropRecord.id == task.crop_record_id).first()
        plot = db.query(Plot).filter(Plot.id == crop_record.plot_id).first() if crop_record else None

        result.append({
            "id": task.id,
            "task_type": task.task_type,
            "scheduled_date": task.scheduled_date,
            "completed_date": task.completed_date,
            "status": task.status,
            "description": task.description,
            "plot_name": plot.name if plot else "",
            "crop_name": crop_record.crop_name if crop_record else ""
        })

    return result


@router.post("/tasks", response_model=FarmTaskResponse)
def create_task(task: FarmTaskCreate, db: Session = Depends(get_db)):
    """创建农事任务"""
    db_task = FarmTask(
        crop_record_id=task.crop_record_id,
        task_type=task.task_type,
        scheduled_date=task.scheduled_date,
        description=task.description,
        status="pending"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/tasks/{task_id}/complete", response_model=MessageResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    """完成任务"""
    task = db.query(FarmTask).filter(FarmTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    from datetime import datetime
    task.status = "completed"
    task.completed_date = datetime.utcnow()
    db.commit()

    return MessageResponse(message="任务已完成")
