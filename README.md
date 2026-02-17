# Keep-Alive Service for Nova Library Backend

A Flask app deployed on Vercel that pings the Nova Library Backend health endpoint every minute to keep it awake.

## Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy to Vercel:
```bash
vercel
```

3. Follow the prompts to link your project

## Endpoints

- `/` - Home page showing service status
- `/api/ping` - Manually trigger a health check (also called by cron)

## How it works

Vercel Cron Jobs automatically call `/api/ping` every minute, which then pings the Nova Library Backend health endpoint.

Note: Vercel's free tier cron jobs run every minute minimum. For 30-second intervals, consider upgrading or using a different platform.
