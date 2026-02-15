"""
Vercel Serverless Function Entry Point
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

from app.config import settings
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="智慧农业管理系统后端API"
)

# Configure CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.api import sensors, plots, disease, analysis, forecast

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
        "docs": "/api/docs"
    }


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


# Vercel serverless handler
handler = app
