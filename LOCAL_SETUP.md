# Local Development Setup Guide

## Prerequisites

### Required Software
1. **Python 3.9+**
2. **Node.js 18+**
3. **PostgreSQL** (or use SQLite for testing)
4. **Redis** (optional, for caching)
5. **Git**

### Hardware Requirements
- **GPU**: NVIDIA GPU with CUDA support (recommended)
- **VRAM**: 6GB minimum, 16GB recommended
- **RAM**: 16GB+ recommended
- **Storage**: 10GB+ free space

## Step 1: Backend Setup

### 1.1 Create Virtual Environment
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 1.2 Install Dependencies
```bash
# Install basic requirements
pip install --upgrade pip
pip install -r requirements.txt

# If you encounter issues with Hunyuan3D-2, install it separately:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate
pip install trimesh pymeshlab pygltflib
```

### 1.3 Setup Environment
```bash
# Copy environment file
cp .env.example .env

# Edit the .env file with your settings
# For local testing, you can use SQLite instead of PostgreSQL:
# DATABASE_URL=sqlite:///./hunyuan3d.db
```

### 1.4 Initialize Database (SQLite)
```bash
# If using SQLite, create the database file
python -c "
from app.core.database import engine, Base
Base.metadata.create_all(bind=engine)
print('Database created successfully!')
"
```

### 1.5 Test Backend
```bash
# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# You should see output like:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete.
```

### 1.6 Test Backend API
Open your browser and visit:
- **API Root**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs

## Step 2: Frontend Setup

### 2.1 Install Dependencies
```bash
cd frontend

# Install Node.js dependencies
npm install

# If you encounter issues, try:
npm install --legacy-peer-deps
```

### 2.2 Setup Environment
```bash
# Copy environment file
cp .env.example .env

# Edit .env.local (create if it doesn't exist):
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### 2.3 Fix TypeScript Issues (if needed)
Create a `tsconfig.json` if missing:
```bash
npm run build # This will create necessary config files
```

### 2.4 Start Frontend
```bash
# Start the development server
npm run dev

# You should see output like:
#   ✓ Ready in 2.5s
#   - Local: http://localhost:3000
```

## Step 3: Test the Application

### 3.1 Access the Application
Open your browser and visit: **http://localhost:3000**

### 3.2 Test Model Generation
1. Navigate to the "Generate" tab
2. Enter a text prompt like: "a simple red cube"
3. Click "Generate Model"
4. Check the browser console for any errors

### 3.3 Check Backend Logs
Monitor the backend terminal for:
- Model loading progress
- GPU availability
- Generation status
- Any error messages

## Troubleshooting Common Issues

### Issue 1: Hunyuan3D-2 Not Found
```bash
# Install Hunyuan3D-2 manually
pip install git+https://github.com/Tencent-Hunyuan/Hunyuan3D-2.git

# Or install from PyPI if available
pip install hunyuan3d
```

### Issue 2: GPU Not Detected
```bash
# Check CUDA availability
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
python -c "import torch; print('GPU count:', torch.cuda.device_count())"

# If false, install CUDA drivers or use CPU mode
```

### Issue 3: Frontend Build Errors
```bash
# Install missing dependencies
npm install @types/node @types/react @types/react-dom
npm install tailwind-merge clsx

# Or use legacy peer deps
npm install --legacy-peer-deps
```

### Issue 4: Database Connection Issues
```bash
# Use SQLite for local testing
# In backend/.env:
DATABASE_URL=sqlite:///./hunyuan3d.db

# Then create database:
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### Issue 5: Port Conflicts
```bash
# Change ports if needed
# Backend: uvicorn main:app --port 8001
# Frontend: npm run dev -- -p 3001

# Update frontend .env.local:
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## Step 4: Test with Minimal Setup

If you're having issues, try this minimal test first:

### Backend Test
```python
# Create test_backend.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Backend is working!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run with: `python test_backend.py`

### Frontend Test
```javascript
// Create a simple test page
// In frontend/app/page.tsx:
export default function Home() {
  return (
    <div>
      <h1>Frontend is working!</h1>
      <p>API URL: {process.env.NEXT_PUBLIC_API_URL}</p>
    </div>
  )
}
```

## Step 5: Verify Full Integration

Once both servers are running:

1. **Backend Health**: http://localhost:8000/health
2. **Frontend**: http://localhost:3000
3. **API Docs**: http://localhost:8000/docs
4. **Test API Call**:
```bash
curl http://localhost:8000/health
```

## Next Steps After Setup

1. **Test with Simple Prompts**: Start with basic 3D objects
2. **Check GPU Usage**: Monitor GPU memory during generation
3. **Review Logs**: Check for any warnings or errors
4. **Optimize Settings**: Adjust VRAM and quality settings as needed

## Getting Help

If you encounter issues:

1. **Check the logs** in both backend and frontend terminals
2. **Verify GPU availability** with CUDA
3. **Test with minimal setup** first
4. **Check environment variables** in .env files
5. **Ensure all dependencies are installed**

## Quick Commands Reference

```bash
# Backend
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev

# Test
curl http://localhost:8000/health
# Open http://localhost:3000
```
