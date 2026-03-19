# Hunyuan3D-2 Web Application Setup Guide

## Prerequisites

### Hardware Requirements
- **GPU**: NVIDIA GPU with CUDA support (recommended: RTX 3080 or better)
- **VRAM**: Minimum 6GB (shape only), 16GB+ recommended (shape + texture)
- **RAM**: 16GB+ recommended
- **Storage**: 50GB+ free space

### Software Requirements
- **Docker**: 20.10+ with Docker Compose
- **NVIDIA Docker**: For GPU support
- **Git**: For cloning the repository
- **Node.js**: 18+ (for local development)
- **Python**: 3.9+ (for local development)

## Quick Start with Docker

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hunyuan3d-webapp
```

### 2. Install NVIDIA Docker (if not already installed)
```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### 3. Configure Environment
```bash
# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit the files with your configuration
nano backend/.env
nano frontend/.env
```

### 4. Start the Application
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Local Development Setup

### Backend Setup

1. **Create Virtual Environment**
```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Hunyuan3D-2**
```bash
# Install custom rasterizers
cd hy3dgen/texgen/custom_rasterizer
python setup.py install

cd ../../..
cd hy3dgen/texgen/differentiable_renderer
python setup.py install

cd ../../..
```

4. **Setup Database**
```bash
# Install PostgreSQL and Redis first
# Then run migrations
alembic upgrade head
```

5. **Start Backend**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Start Frontend**
```bash
npm run dev
```

## Configuration

### Backend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost/hunyuan3d` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `SECRET_KEY` | JWT secret key | Change in production |
| `OPENAI_API_KEY` | OpenAI API key for AI editing | Required for editing |
| `HUNYUAN_MODEL_PATH` | Hunyuan3D-2 model path | `tencent/Hunyuan3D-2` |
| `LOW_VRAM_MODE` | Enable low VRAM mode | `true` |

### Frontend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |

## GPU Configuration

### CUDA Setup
1. Install NVIDIA drivers
2. Install CUDA Toolkit (11.8+)
3. Install cuDNN
4. Verify installation:
```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

### Low VRAM Mode
If you have limited VRAM, enable low VRAM mode:
```bash
# In backend/.env
LOW_VRAM_MODE=true
ENABLE_FLASHVDM=true
```

## Model Management

### Downloading Models
The application will automatically download Hunyuan3D-2 models on first use. Models are cached in:
- Docker: `model_cache` volume
- Local: `backend/models/`

### Model Variants
- **Hunyuan3D-2**: Full quality (16GB VRAM)
- **Hunyuan3D-2mini**: Reduced quality (6GB VRAM)
- **Hunyuan3D-2mv**: Multi-view optimized

## Troubleshooting

### Common Issues

#### GPU Not Detected
```bash
# Check GPU availability
nvidia-smi

# Check CUDA in Python
python -c "import torch; print(torch.cuda.is_available())"
```

#### Out of Memory Errors
1. Enable low VRAM mode
2. Reduce batch size
3. Use smaller model variant

#### Connection Errors
1. Check if all services are running: `docker-compose ps`
2. Verify network connectivity
3. Check firewall settings

#### Model Loading Issues
1. Clear model cache
2. Check internet connection
3. Verify Hugging Face access

### Logs

#### Docker Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f backend
```

#### Local Development Logs
- Backend: Console output
- Frontend: Browser console and terminal

## Performance Optimization

### Backend
- Use GPU acceleration
- Enable model caching
- Optimize database queries
- Use Redis for caching

### Frontend
- Enable code splitting
- Optimize 3D rendering
- Use lazy loading
- Compress assets

## Security

### Production Checklist
- [ ] Change default passwords
- [ ] Use HTTPS
- [ ] Set up firewall
- [ ] Enable rate limiting
- [ ] Use environment variables for secrets
- [ ] Regular security updates

### API Security
- JWT authentication
- CORS configuration
- Input validation
- File upload restrictions

## Monitoring

### Health Checks
- Backend: `/health` endpoint
- Frontend: Application health
- Database: Connection status
- GPU: Memory usage

### Metrics
- Generation time
- Model size
- User activity
- Error rates

## Backup and Recovery

### Database Backup
```bash
# PostgreSQL backup
pg_dump hunyuan3d > backup.sql

# Restore
psql hunyuan3d < backup.sql
```

### Model Backup
```bash
# Backup cached models
cp -r backend/models/ backup/models/
```

## Scaling

### Horizontal Scaling
- Load balancer setup
- Multiple backend instances
- Database replication
- Redis clustering

### Vertical Scaling
- GPU upgrades
- Memory increases
- Storage expansion

## Support

### Documentation
- [API Documentation](http://localhost:8000/docs)
- [Hunyuan3D-2 GitHub](https://github.com/Tencent-Hunyuan/Hunyuan3D-2)
- [Three.js Documentation](https://threejs.org/docs/)

### Community
- GitHub Issues
- Discord Server
- Stack Overflow

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
