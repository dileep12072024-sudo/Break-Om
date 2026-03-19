"""
API endpoints for 3D model generation and management
"""
import io
import uuid
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.schemas.model import (
    GenerationRequest, 
    EditRequest, 
    GenerationResponse, 
    ModelResponse,
    ModelListResponse,
    ErrorResponse
)
from app.models.model import Model3D, ModelEdit
from app.models.user import User
from app.services.hunyuan_service import HunyuanService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate", response_model=GenerationResponse)
async def generate_model(
    request: GenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a 3D model from text prompt
    """
    try:
        # Get Hunyuan service from app state
        from fastapi import FastAPI
        app = FastAPI()
        hunyuan_service = app.state.hunyuan_service
        
        # Generate unique model ID
        model_id = str(uuid.uuid4())
        
        logger.info(f"Generating model {model_id} from prompt: {request.prompt}")
        
        # Generate 3D model
        model_data = hunyuan_service.generate_from_text(
            prompt=request.prompt,
            generate_texture=request.generate_texture
        )
        
        # Save to database
        db_model = Model3D(
            model_id=model_id,
            user_id=1,  # TODO: Get from authenticated user
            prompt=request.prompt,
            format=request.format.value,
            file_data=model_data,
            file_size=len(model_data),
            status="completed"
        )
        
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        
        return GenerationResponse(
            success=True,
            model_id=model_id,
            message="Model generated successfully",
            download_url=f"/api/v1/models/{model_id}/download"
        )
        
    except Exception as e:
        logger.error(f"Failed to generate model: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Model generation failed: {str(e)}"
        )


@router.post("/generate-from-image", response_model=GenerationResponse)
async def generate_model_from_image(
    file: UploadFile = File(...),
    generate_texture: bool = True,
    format: str = "glb",
    db: Session = Depends(get_db)
):
    """
    Generate a 3D model from uploaded image
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Read image data
        image_data = await file.read()
        
        # Get Hunyuan service
        from fastapi import FastAPI
        app = FastAPI()
        hunyuan_service = app.state.hunyuan_service
        
        # Generate unique model ID
        model_id = str(uuid.uuid4())
        
        logger.info(f"Generating model {model_id} from image")
        
        # Generate 3D model
        model_data = hunyuan_service.generate_from_image(
            image_data=image_data,
            generate_texture=generate_texture
        )
        
        # Save to database
        db_model = Model3D(
            model_id=model_id,
            user_id=1,  # TODO: Get from authenticated user
            prompt=f"Generated from image: {file.filename}",
            format=format,
            file_data=model_data,
            file_size=len(model_data),
            status="completed"
        )
        
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        
        return GenerationResponse(
            success=True,
            model_id=model_id,
            message="Model generated successfully from image",
            download_url=f"/api/v1/models/{model_id}/download"
        )
        
    except Exception as e:
        logger.error(f"Failed to generate model from image: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Model generation failed: {str(e)}"
        )


@router.post("/edit", response_model=GenerationResponse)
async def edit_model(
    request: EditRequest,
    db: Session = Depends(get_db)
):
    """
    Edit an existing 3D model using AI
    """
    try:
        # Get original model from database
        db_model = db.query(Model3D).filter(
            Model3D.model_id == request.model_id
        ).first()
        
        if not db_model:
            raise HTTPException(
                status_code=404,
                detail="Model not found"
            )
        
        # Get Hunyuan service
        from fastapi import FastAPI
        app = FastAPI()
        hunyuan_service = app.state.hunyuan_service
        
        logger.info(f"Editing model {request.model_id} with prompt: {request.edit_prompt}")
        
        # Edit the model
        edited_model_data = hunyuan_service.edit_model(
            model_data=db_model.file_data,
            edit_prompt=request.edit_prompt
        )
        
        # Create edit history record
        edit_record = ModelEdit(
            model_id=request.model_id,
            user_id=1,  # TODO: Get from authenticated user
            edit_prompt=request.edit_prompt,
            original_file_data=db_model.file_data,
            edited_file_data=edited_model_data,
            status="completed"
        )
        
        db.add(edit_record)
        
        # Update the original model
        db_model.file_data = edited_model_data
        db_model.file_size = len(edited_model_data)
        db_model.prompt = f"{db_model.prompt} | Edited: {request.edit_prompt}"
        
        db.commit()
        db.refresh(db_model)
        
        return GenerationResponse(
            success=True,
            model_id=request.model_id,
            message="Model edited successfully",
            download_url=f"/api/v1/models/{request.model_id}/download"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to edit model: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Model editing failed: {str(e)}"
        )


@router.get("/{model_id}/download")
async def download_model(
    model_id: str,
    format: Optional[str] = "glb",
    db: Session = Depends(get_db)
):
    """
    Download a 3D model in specified format
    """
    try:
        # Get model from database
        db_model = db.query(Model3D).filter(
            Model3D.model_id == model_id
        ).first()
        
        if not db_model:
            raise HTTPException(
                status_code=404,
                detail="Model not found"
            )
        
        # Get Hunyuan service for format conversion
        from fastapi import FastAPI
        app = FastAPI()
        hunyuan_service = app.state.hunyuan_service
        
        # Convert to requested format if needed
        if format != db_model.format:
            model_data = hunyuan_service.export_model(
                model_data=db_model.file_data,
                format=format
            )
        else:
            model_data = db_model.file_data
        
        # Return file as streaming response
        filename = f"{model_id}.{format}"
        
        return StreamingResponse(
            io.BytesIO(model_data),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Download failed: {str(e)}"
        )


@router.get("/", response_model=ModelListResponse)
async def list_models(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    """
    List user's 3D models
    """
    try:
        # TODO: Filter by authenticated user
        query = db.query(Model3D)
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        models = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # Convert to response format
        model_responses = [
            ModelResponse(
                model_id=model.model_id,
                prompt=model.prompt,
                format=model.format,
                file_size=model.file_size,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in models
        ]
        
        return ModelListResponse(
            models=model_responses,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list models: {str(e)}"
        )


@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: str,
    db: Session = Depends(get_db)
):
    """
    Get model details
    """
    try:
        # Get model from database
        db_model = db.query(Model3D).filter(
            Model3D.model_id == model_id
        ).first()
        
        if not db_model:
            raise HTTPException(
                status_code=404,
                detail="Model not found"
            )
        
        return ModelResponse(
            model_id=db_model.model_id,
            prompt=db_model.prompt,
            format=db_model.format,
            file_size=db_model.file_size,
            created_at=db_model.created_at,
            updated_at=db_model.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get model: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get model: {str(e)}"
        )


@router.delete("/{model_id}")
async def delete_model(
    model_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a 3D model
    """
    try:
        # Get model from database
        db_model = db.query(Model3D).filter(
            Model3D.model_id == model_id
        ).first()
        
        if not db_model:
            raise HTTPException(
                status_code=404,
                detail="Model not found"
            )
        
        # Delete the model
        db.delete(db_model)
        db.commit()
        
        return {"message": "Model deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete model: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete model: {str(e)}"
        )
