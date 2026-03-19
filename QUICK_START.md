# Quick Start Guide - Local Server Setup

## Step 1: Start Backend (Simple Version)

Open a NEW terminal window and run:

```bash
cd c:\3D\backend
venv\Scripts\activate
python simple_test.py
```

You should see:
```
Starting server on http://localhost:8000
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 2: Test Backend

Open your browser and test:
- **Backend Test**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

You should see JSON responses in both cases.

## Step 3: Start Frontend

Open ANOTHER terminal window and run:

```bash
cd c:\3D\frontend
npm install
npm run dev
```

You should see:
```
- Ready in 2.5s
- Local: http://localhost:3000
```

## Step 4: Test Frontend

Open your browser and go to:
- **Frontend**: http://localhost:3000

## Troubleshooting

### If Backend Doesn't Start:
1. Make sure you're in the correct directory: `cd c:\3D\backend`
2. Activate virtual environment: `venv\Scripts\activate`
3. Check Python version: `python --version`

### If Frontend Doesn't Start:
1. Make sure you're in the correct directory: `cd c:\3D\frontend`
2. Install dependencies: `npm install`
3. Try: `npm run dev -- -p 3001` (if port 3000 is busy)

### If You See "Moved to Another Address":
1. Check if both servers are running
2. Try different ports:
   - Backend: `python -c "import uvicorn; uvicorn.run('simple_test:app', port=8001)"`
   - Frontend: `npm run dev -- -p 3001`
3. Update frontend environment: `echo "NEXT_PUBLIC_API_URL=http://localhost:8001" > .env.local`

### If You See Connection Errors:
1. Check Windows Firewall
2. Try using `127.0.0.1` instead of `localhost`
3. Check if antivirus is blocking the connection

## Quick Commands

```bash
# Terminal 1 - Backend
cd c:\3D\backend
venv\Scripts\activate
python simple_test.py

# Terminal 2 - Frontend  
cd c:\3D\frontend
npm run dev

# Test in browser
# http://localhost:8000  (Backend)
# http://localhost:3000  (Frontend)
```

## Expected Results

✅ Backend at http://localhost:8000 shows: `{"message": "Backend is working!", "status": "ok"}`
✅ Frontend at http://localhost:3000 shows the web application
✅ No "moved to another address" errors
✅ No connection refused errors
