"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Hunyuan3D-2 Web API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/hunyuan3d"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Hunyuan3D-2 Settings
    HUNYUAN_MODEL_PATH: str = "tencent/Hunyuan3D-2"
    HUNYUAN_SUBFOLDER: str = "hunyuan3d-dit-v2-0"
    TEXGEN_MODEL_PATH: str = "tencent/Hunyuan3D-2"
    LOW_VRAM_MODE: bool = True
    ENABLE_FLASHVDM: bool = False
    
    # AI Settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MODELS_DIR: str = "models"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # GPU Settings
    CUDA_VISIBLE_DEVICES: str = "0"
    TORCH_CUDA_ARCH_LIST: Optional[str] = None
    
    # Background Tasks
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.MODELS_DIR, exist_ok=True)
