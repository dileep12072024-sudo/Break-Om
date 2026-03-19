"""
Main FastAPI application for Hunyuan3D-2 Web Application
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
import logging

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import engine, Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting up Hunyuan3D-2 Web Application...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize AI models
    try:
        from app.services.hunyuan_service import HunyuanService
        hunyuan_service = HunyuanService()
        app.state.hunyuan_service = hunyuan_service
        logger.info("Hunyuan3D-2 service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Hunyuan3D-2 service: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Hunyuan3D-2 Web Application...")


# Create FastAPI application
app = FastAPI(
    title="Hunyuan3D-2 Web API",
    description="API for generating and editing 3D models using Hunyuan3D-2",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Hunyuan3D-2 Web API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Hunyuan3D-2 Web API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
