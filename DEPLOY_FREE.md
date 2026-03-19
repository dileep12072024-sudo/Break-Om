# Free Deployment

This project can be deployed publicly at zero cost in demo mode using:

- Frontend: Vercel Hobby
- Backend: Render Free

This deploys the current web app with the lightweight mock backend in `backend/test_server.py`. It is suitable for demos and testing, not the full GPU-backed Hunyuan pipeline.

## What gets deployed

- Public frontend from `frontend/`
- Public backend API from `backend/test_server.py`
- Frontend talks to backend through `NEXT_PUBLIC_API_URL`

## 1. Push this project to GitHub

From the project root:

```bash
cd /mnt/c/3D
git init
git add .
git commit -m "Prepare free deployment"
```

Then create a GitHub repo and push:

```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

## 2. Deploy the backend on Render

1. Sign in to Render.
2. Create a new Web Service from the GitHub repo.
3. Render should detect `render.yaml` automatically.
4. Deploy the service.

Expected backend URL:

```text
https://hunyuan3d-demo-backend.onrender.com
```

Health endpoint:

```text
https://<your-render-url>/health
```

## 3. Deploy the frontend on Vercel

1. Sign in to Vercel.
2. Import the same GitHub repo.
3. Set the Root Directory to `frontend`.
4. Add this environment variable:

```text
NEXT_PUBLIC_API_URL=https://<your-render-url>
```

5. Deploy.

Expected frontend URL:

```text
https://<your-vercel-project>.vercel.app
```

## 4. Result

Open the Vercel URL only. The frontend will call the Render backend automatically, so it behaves as one web application.

## Important limitations

- Render free services can sleep after inactivity, so the first backend request may be slow.
- This free deployment uses the mock backend, not the real Hunyuan GPU pipeline.
- For a true production-grade always-on app, you would need a paid backend or your own server.
