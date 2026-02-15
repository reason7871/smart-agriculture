from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.config import settings
from app.database import engine, Base
from app.api import sensors, plots, disease, analysis, forecast

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建上传目录
os.makedirs("uploads/disease", exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="智慧农业管理系统后端API"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(sensors.router, prefix="/api")
app.include_router(plots.router, prefix="/api")
app.include_router(disease.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(forecast.router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "智慧农业管理系统 API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
