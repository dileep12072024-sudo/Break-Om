"""
Hunyuan3D-2 integration service for 3D model generation and editing
"""
import os
import base64
import io
import logging
from typing import Optional, Tuple, Dict, Any
import torch
import trimesh
from PIL import Image
import numpy as np

# Hunyuan3D-2 imports
try:
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
    from hy3dgen.texgen import Hunyuan3DPaintPipeline
    HUNYUAN_AVAILABLE = True
except ImportError:
    logging.warning("Hunyuan3D-2 not available. Please install it first.")
    HUNYUAN_AVAILABLE = False

from app.core.config import settings

logger = logging.getLogger(__name__)


class HunyuanService:
    """Service for Hunyuan3D-2 operations"""
    
    def __init__(self):
        """Initialize Hunyuan3D-2 pipelines"""
        if not HUNYUAN_AVAILABLE:
            raise ImportError("Hunyuan3D-2 is not installed")
        
        self.shape_pipeline = None
        self.texture_pipeline = None
        self.device = self._get_device()
        
        # Initialize pipelines
        self._initialize_pipelines()
    
    def _get_device(self) -> str:
        """Get the best available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def _initialize_pipelines(self):
        """Initialize Hunyuan3D-2 pipelines"""
        try:
            logger.info("Initializing Hunyuan3D-2 shape generation pipeline...")
            self.shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
                settings.HUNYUAN_MODEL_PATH,
                subfolder=settings.HUNYUAN_SUBFOLDER,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None,
                low_vram_mode=settings.LOW_VRAM_MODE,
                device_map="auto" if self.device == "cuda" else None
            )
            
            logger.info("Initializing Hunyuan3D-2 texture generation pipeline...")
            self.texture_pipeline = Hunyuan3DPaintPipeline.from_pretrained(
                settings.TEXGEN_MODEL_PATH,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                variant="fp16" if self.device == "cuda" else None,
                low_vram_mode=settings.LOW_VRAM_MODE,
                device_map="auto" if self.device == "cuda" else None
            )
            
            logger.info(f"Hunyuan3D-2 pipelines initialized successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Hunyuan3D-2 pipelines: {e}")
            raise
    
    def generate_from_text(self, prompt: str, generate_texture: bool = True) -> bytes:
        """
        Generate 3D model from text prompt
        
        Args:
            prompt: Text description of the 3D model
            generate_texture: Whether to generate texture
            
        Returns:
            GLB file as bytes
        """
        try:
            logger.info(f"Generating 3D model from prompt: {prompt}")
            
            # For text-to-3D, we need to first create a simple image representation
            # This is a simplified approach - in production, you might want to use
            # a text-to-image model first
            dummy_image = self._create_dummy_image_from_prompt(prompt)
            
            # Generate shape
            mesh = self.shape_pipeline(image=dummy_image)[0]
            
            # Generate texture if requested
            if generate_texture and self.texture_pipeline:
                mesh = self.texture_pipeline(mesh, image=dummy_image)
            
            # Convert to GLB format
            glb_data = self._mesh_to_glb(mesh)
            
            logger.info("3D model generated successfully")
            return glb_data
            
        except Exception as e:
            logger.error(f"Failed to generate 3D model: {e}")
            raise
    
    def generate_from_image(self, image_data: bytes, generate_texture: bool = True) -> bytes:
        """
        Generate 3D model from image
        
        Args:
            image_data: Image file as bytes
            generate_texture: Whether to generate texture
            
        Returns:
            GLB file as bytes
        """
        try:
            logger.info("Generating 3D model from image")
            
            # Load image
            image = Image.open(io.BytesIO(image_data))
            
            # Generate shape
            mesh = self.shape_pipeline(image=image)[0]
            
            # Generate texture if requested
            if generate_texture and self.texture_pipeline:
                mesh = self.texture_pipeline(mesh, image=image)
            
            # Convert to GLB format
            glb_data = self._mesh_to_glb(mesh)
            
            logger.info("3D model generated successfully from image")
            return glb_data
            
        except Exception as e:
            logger.error(f"Failed to generate 3D model from image: {e}")
            raise
    
    def edit_model(self, model_data: bytes, edit_prompt: str) -> bytes:
        """
        Edit existing 3D model using AI
        
        Args:
            model_data: GLB file as bytes
            edit_prompt: Text description of edits to make
            
        Returns:
            Edited GLB file as bytes
        """
        try:
            logger.info(f"Editing 3D model with prompt: {edit_prompt}")
            
            # Load existing mesh
            mesh = self._glb_to_mesh(model_data)
            
            # Process edit prompt to determine modifications
            modifications = self._parse_edit_prompt(edit_prompt)
            
            # Apply modifications (simplified approach)
            edited_mesh = self._apply_modifications(mesh, modifications)
            
            # Convert back to GLB
            glb_data = self._mesh_to_glb(edited_mesh)
            
            logger.info("3D model edited successfully")
            return glb_data
            
        except Exception as e:
            logger.error(f"Failed to edit 3D model: {e}")
            raise
    
    def _create_dummy_image_from_prompt(self, prompt: str) -> Image.Image:
        """Create a simple placeholder image from text prompt"""
        # This is a simplified approach
        # In production, you'd use a text-to-image model
        size = (512, 512)
        image = Image.new('RGB', size, color='gray')
        return image
    
    def _mesh_to_glb(self, mesh: trimesh.Trimesh) -> bytes:
        """Convert trimesh object to GLB bytes"""
        try:
            # Export to GLB format
            glb_buffer = io.BytesIO()
            mesh.export(glb_buffer, file_type='glb')
            return glb_buffer.getvalue()
        except Exception as e:
            logger.error(f"Failed to convert mesh to GLB: {e}")
            raise
    
    def _glb_to_mesh(self, glb_data: bytes) -> trimesh.Trimesh:
        """Convert GLB bytes to trimesh object"""
        try:
            glb_buffer = io.BytesIO(glb_data)
            mesh = trimesh.load(glb_buffer, file_type='glb')
            return mesh
        except Exception as e:
            logger.error(f"Failed to convert GLB to mesh: {e}")
            raise
    
    def _parse_edit_prompt(self, prompt: str) -> Dict[str, Any]:
        """Parse edit prompt to extract modifications"""
        # This is a simplified parser
        # In production, you'd use AI to parse and understand the modifications
        modifications = {
            "scale": 1.0,
            "rotation": [0, 0, 0],
            "texture_changes": [],
            "geometry_changes": []
        }
        
        prompt_lower = prompt.lower()
        
        # Simple keyword-based modifications
        if "bigger" in prompt_lower or "larger" in prompt_lower:
            modifications["scale"] = 1.2
        elif "smaller" in prompt_lower:
            modifications["scale"] = 0.8
        
        if "rotate" in prompt_lower:
            modifications["rotation"] = [0, 45, 0]  # Simple rotation
        
        return modifications
    
    def _apply_modifications(self, mesh: trimesh.Trimesh, modifications: Dict[str, Any]) -> trimesh.Trimesh:
        """Apply modifications to mesh"""
        try:
            # Apply scaling
            if modifications["scale"] != 1.0:
                mesh.apply_scale(modifications["scale"])
            
            # Apply rotation
            if any(modifications["rotation"]):
                from trimesh.transformations import rotation_matrix
                rotation = rotation_matrix(
                    np.radians(modifications["rotation"][1]), 
                    [0, 1, 0]
                )
                mesh.apply_transform(rotation)
            
            return mesh
            
        except Exception as e:
            logger.error(f"Failed to apply modifications: {e}")
            raise
    
    def export_model(self, model_data: bytes, format: str = "glb") -> bytes:
        """
        Export model in different formats
        
        Args:
            model_data: GLB file as bytes
            format: Export format (glb, obj, fbx)
            
        Returns:
            Exported file as bytes
        """
        try:
            mesh = self._glb_to_mesh(model_data)
            
            # Export in requested format
            buffer = io.BytesIO()
            mesh.export(buffer, file_type=format)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Failed to export model as {format}: {e}")
            raise
