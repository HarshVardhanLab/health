# Keep-Alive Service for Nova Library Backend

A Flask app deployed on Railway that pings the Nova Library Backend health endpoint every 30 seconds to keep it awake.

## Deployment on Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will automatically detect and deploy your Flask app

## Endpoints

- `/` - Home page with animated smiley face
- `/api/ping` - Manually trigger a health check

## How it works

The app runs a background thread that automatically pings the Nova Library Backend health endpoint every 30 seconds, keeping it awake.

## Local Development

```bash
pip install -r requirements.txt
python app.py
```
