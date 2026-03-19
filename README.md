# Hunyuan3D-2 Web Application

A modern web application for generating and editing textured 3D models using Tencent's Hunyuan3D-2 AI model.

## Features

- **Text-to-3D Generation**: Generate high-quality 3D models from text prompts
- **Interactive 3D Viewer**: Rotate, zoom, and pan models in the browser
- **AI-Assisted Editing**: Modify models using natural language commands
- **Export Support**: Download models in GLTF, OBJ, and FBX formats
- **User Authentication**: Secure login and model management
- **Real-time Processing**: Fast generation with GPU acceleration support

## Architecture

```
├── frontend/          # Next.js 14 + Three.js
├── backend/           # Python FastAPI + Hunyuan3D-2
├── shared/            # Shared types and utilities
├── docker/            # Docker configurations
└── docs/              # Documentation
```

## Tech Stack

### Frontend
- Next.js 14 with TypeScript
- Three.js for 3D rendering
- Tailwind CSS for styling
- Zustand for state management
- React Hook Form for forms

### Backend
- Python 3.9+
- FastAPI for REST API
- Hunyuan3D-2 for 3D generation
- PostgreSQL for database
- Redis for caching
- Celery for background tasks

### AI Integration
- OpenAI GPT-4 for text processing
- Hunyuan3D-2 for 3D model generation
- Custom editing pipeline for modifications

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- CUDA-compatible GPU (recommended)
- Docker (optional)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd hunyuan3d-webapp
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Environment Configuration**
```bash
# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Edit with your configuration
```

5. **Database Setup**
```bash
cd backend
alembic upgrade head
```

6. **Run the Application**
```bash
# Backend (Terminal 1)
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (Terminal 2)
cd frontend
npm run dev
```

Visit http://localhost:3000 to access the application.

## Docker Deployment

```bash
docker-compose up -d
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## Model Requirements

- **VRAM**: 6GB minimum (shape only), 16GB recommended (shape + texture)
- **GPU**: CUDA-compatible with compute capability 7.0+
- **RAM**: 16GB+ recommended
- **Storage**: 10GB+ for models and cache

## Usage Examples

### Generate a 3D Model
```python
# Via API
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a detailed dragon with metallic scales"}'
```

### Edit a Model
```python
# Via API
curl -X POST "http://localhost:8000/api/v1/edit" \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "model_123",
    "prompt": "make the wings longer and add fire effects"
  }'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Tencent Hunyuan3D-2](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) for the amazing 3D generation model
- [Three.js](https://threejs.org/) for 3D rendering capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
