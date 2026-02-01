# Deployment Guide

This guide covers deploying Repofiy Bot to Railway and Vercel.

## Railway Deployment

### Prerequisites
- Railway account (https://railway.app)
- GitHub repository connected to Railway
- Environment variables ready

### Steps

1. **Create a new project** on Railway
2. **Connect your GitHub repository**
3. **Configure environment variables** in Railway dashboard:
   ```
   GITHUB_TOKEN=your_token
   REPO_OWNER=your_owner
   REPO_NAME=your_repo
   ```
4. **Railway detects Dockerfile** and automatically deploys

### Notes
- Ensure `Dockerfile` references correct filenames (`repofiy_bot.py`)
- `requirements.txt` must be in root directory
- Logs available in Railway dashboard under "Deployments"

## Vercel Deployment

Vercel is designed for serverless functions and API deployment. For a continuous bot, Railway is recommended.

If you want to expose your bot as an API:

1. Create an API handler in a `api/` directory
2. Deploy using Vercel CLI: `vercel deploy`
3. Use cron jobs for scheduled tasks (Vercel Pro)

## Docker Build Troubleshooting

**Error: File not found**
- Verify all filenames match in `Dockerfile` COPY commands
- Check working directory context

**Error: Port already in use**
- Change port in bot configuration or use PORT environment variable

## Testing Locally

```bash
docker build -t repofiy-bot .
docker run -e GITHUB_TOKEN=your_token repofiy-bot
```
