# Local Windows GPU Setup

This is the fastest path to get real image-to-3D generation working from this repo.

## Requirements

- Windows machine with NVIDIA GPU
- Recent NVIDIA driver
- Python 3.10 or 3.11
- Node.js 18+
- Git

## 1. Backend setup

Open PowerShell in `C:\3D\backend`.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
pip install git+https://github.com/Tencent-Hunyuan/Hunyuan3D-2.git
Copy-Item .env.example .env
```

Edit `.env` if needed. The defaults now use SQLite locally.

## 2. Verify GPU

```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no-gpu')"
```

If this prints `False`, the real pipeline will not run correctly.

## 3. Start the real backend

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000
```

On first startup, model download and initialization can take a long time.

## 4. Frontend setup

Open a second PowerShell in `C:\3D\frontend`.

```powershell
npm install
Set-Content .env.local "NEXT_PUBLIC_API_URL=http://localhost:8000"
npm run dev
```

Open `http://localhost:3000`.

## 5. Use image-to-3D

In the app:

1. Choose `Image to 3D`
2. Upload an image
3. Click `Generate Model`

## Notes

- This path is for local GPU use, not Render free hosting.
- First-run model downloads can be many GB and take time.
- If Hunyuan installation fails, the backend will not start until that package is installed correctly.
