"""
Mock local backend for running the web app without the full Hunyuan stack.
"""
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _cube_obj(name: str) -> bytes:
    safe_name = name.replace("\n", " ").strip() or "Mock Cube"
    content = f"""# {safe_name}
o MockCube
v -1 -1 -1
v 1 -1 -1
v 1 1 -1
v -1 1 -1
v -1 -1 1
v 1 -1 1
v 1 1 1
v -1 1 1
f 1 2 3 4
f 5 8 7 6
f 1 5 6 2
f 2 6 7 3
f 3 7 8 4
f 5 1 4 8
"""
    return content.encode("utf-8")


class GenerationRequest(BaseModel):
    prompt: str
    generate_texture: bool = True
    format: str = "glb"


class EditRequest(BaseModel):
    model_id: str
    edit_prompt: str
    format: Optional[str] = "obj"


class StoredModel(BaseModel):
    model_id: str
    prompt: str
    format: str
    file_size: int
    created_at: str
    updated_at: str
    file_data: bytes


MODELS: Dict[str, StoredModel] = {}


def _store_model(prompt: str) -> StoredModel:
    model_id = str(uuid4())
    created_at = _now_iso()
    file_data = _cube_obj(prompt)
    model = StoredModel(
        model_id=model_id,
        prompt=prompt,
        format="obj",
        file_size=len(file_data),
        created_at=created_at,
        updated_at=created_at,
        file_data=file_data,
    )
    MODELS[model_id] = model
    return model


app = FastAPI(
    title="Hunyuan3D-2 Local Mock API",
    description="Mock API for local UI development",
    version="0.2.0",
)

frontend_origin = os.getenv("FRONTEND_ORIGIN")
allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

if frontend_origin:
    allowed_origins.append(frontend_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Hunyuan3D-2 local mock API is running",
        "version": "0.2.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Hunyuan3D-2 local mock API",
        "models_loaded": len(MODELS),
    }


@app.post("/api/v1/models/generate")
async def generate_model(request: GenerationRequest):
    model = _store_model(request.prompt)
    return {
        "success": True,
        "model_id": model.model_id,
        "message": "Mock model generated successfully",
        "download_url": f"/api/v1/models/{model.model_id}/download",
    }


@app.post("/api/v1/models/generate-from-image")
async def generate_model_from_image(
    file: UploadFile = File(...),
    generate_texture: bool = True,
    format: str = "glb",
):
    prompt = f"Image upload: {file.filename or 'untitled image'}"
    model = _store_model(prompt)
    return {
        "success": True,
        "model_id": model.model_id,
        "message": "Mock model generated from image successfully",
        "download_url": f"/api/v1/models/{model.model_id}/download",
    }


@app.post("/api/v1/models/edit")
async def edit_model(request: EditRequest):
    existing = MODELS.get(request.model_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Model not found")

    updated_prompt = f"{existing.prompt} | Edit: {request.edit_prompt}"
    updated_data = _cube_obj(updated_prompt)
    updated = existing.model_copy(
        update={
            "prompt": updated_prompt,
            "format": "obj",
            "file_size": len(updated_data),
            "updated_at": _now_iso(),
            "file_data": updated_data,
        }
    )
    MODELS[request.model_id] = updated
    return {
        "success": True,
        "model_id": request.model_id,
        "message": "Mock model edited successfully",
        "download_url": f"/api/v1/models/{request.model_id}/download",
    }


@app.get("/api/v1/models")
async def list_models(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    sort: str = "created_at",
):
    models: List[StoredModel] = list(MODELS.values())

    reverse = sort != "-created_at"
    if sort in {"created_at", "-created_at"}:
        models.sort(key=lambda item: item.created_at, reverse=reverse)
    elif sort == "file_size":
        models.sort(key=lambda item: item.file_size, reverse=True)
    elif sort == "prompt":
        models.sort(key=lambda item: item.prompt.lower())

    start = (page - 1) * page_size
    end = start + page_size
    paginated = models[start:end]

    return {
        "models": [
            {
                "model_id": model.model_id,
                "prompt": model.prompt,
                "format": model.format,
                "file_size": model.file_size,
                "created_at": model.created_at,
                "updated_at": model.updated_at,
            }
            for model in paginated
        ],
        "total": len(models),
        "page": page,
        "page_size": page_size,
    }


@app.get("/api/v1/models/{model_id}")
async def get_model(model_id: str):
    model = MODELS.get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    return {
        "model_id": model.model_id,
        "prompt": model.prompt,
        "format": model.format,
        "file_size": model.file_size,
        "created_at": model.created_at,
        "updated_at": model.updated_at,
    }


@app.delete("/api/v1/models/{model_id}")
async def delete_model(model_id: str):
    if model_id not in MODELS:
        raise HTTPException(status_code=404, detail="Model not found")
    del MODELS[model_id]
    return {"success": True, "message": "Model deleted successfully"}


@app.get("/api/v1/models/{model_id}/download")
async def download_model(model_id: str, format: str = "obj"):
    model = MODELS.get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    filename = f"{model_id}.obj"
    return Response(
        content=model.file_data,
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
