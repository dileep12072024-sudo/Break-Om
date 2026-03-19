"""
Pydantic schemas for 3D model operations
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ModelFormat(str, Enum):
    """Supported 3D model formats"""
    GLB = "glb"
    OBJ = "obj"
    FBX = "fbx"


class GenerationRequest(BaseModel):
    """Request schema for 3D model generation"""
    prompt: str = Field(..., min_length=1, max_length=1000, description="Text prompt for 3D generation")
    generate_texture: bool = Field(True, description="Whether to generate texture")
    format: ModelFormat = Field(ModelFormat.GLB, description="Output format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "a detailed dragon with metallic scales",
                "generate_texture": True,
                "format": "glb"
            }
        }


class EditRequest(BaseModel):
    """Request schema for 3D model editing"""
    model_id: str = Field(..., description="ID of the model to edit")
    edit_prompt: str = Field(..., min_length=1, max_length=500, description="Text prompt for editing")
    format: ModelFormat = Field(ModelFormat.GLB, description="Output format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_id": "model_123",
                "edit_prompt": "make the wings longer and add fire effects",
                "format": "glb"
            }
        }


class ModelResponse(BaseModel):
    """Response schema for model operations"""
    model_id: str = Field(..., description="Unique identifier for the model")
    prompt: str = Field(..., description="Original prompt used")
    format: ModelFormat = Field(..., description="Model format")
    file_size: int = Field(..., description="File size in bytes")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_id": "model_123",
                "prompt": "a detailed dragon with metallic scales",
                "format": "glb",
                "file_size": 1048576,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": None
            }
        }


class GenerationResponse(BaseModel):
    """Response schema for generation requests"""
    success: bool = Field(..., description="Whether generation was successful")
    model_id: Optional[str] = Field(None, description="ID of generated model")
    message: str = Field(..., description="Status message")
    download_url: Optional[str] = Field(None, description="URL to download the model")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "model_id": "model_123",
                "message": "Model generated successfully",
                "download_url": "/api/v1/models/model_123/download"
            }
        }


class ErrorResponse(BaseModel):
    """Response schema for errors"""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Generation failed",
                "details": "GPU memory insufficient"
            }
        }


class ModelListResponse(BaseModel):
    """Response schema for model list"""
    models: List[ModelResponse] = Field(..., description="List of models")
    total: int = Field(..., description="Total number of models")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of models per page")
    
    class Config:
        json_schema_extra = {
            "example": {
                "models": [],
                "total": 10,
                "page": 1,
                "page_size": 10
            }
        }
