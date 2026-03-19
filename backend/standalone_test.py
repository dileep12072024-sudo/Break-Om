"""
Standalone test - no virtual environment needed
Just run: python standalone_test.py
"""
try:
    from fastapi import FastAPI
    import uvicorn
    
    app = FastAPI(title="Hunyuan3D-2 Test")
    
    @app.get("/")
    async def root():
        return {"message": "Backend is working!", "status": "ok", "port": 8000}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": "Hunyuan3D-2 Test"}
    
    if __name__ == "__main__":
        print("=" * 50)
        print("STARTING HUNYUAN3D-2 BACKEND SERVER")
        print("=" * 50)
        print("Backend will be available at:")
        print("  - http://localhost:8000")
        print("  - http://127.0.0.1:8000")
        print("=" * 50)
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Please install: pip install fastapi uvicorn")
    print("Or run: pip install -r requirements.txt")
