# Railway Deployment Guide

## Deploy to Railway (Free Tier)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"

### Step 2: Connect Repository
1. Select your repository: `rihanpathan2425/voice-ai-agent`
2. Railway will auto-detect Python project
3. Click "Deploy"

### Step 3: Add Environment Variables
Go to Settings → Variables and add:
```
BOT_TOKEN=your_telegram_bot_token
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_HOST=http://host.docker.internal:11434
ENABLE_TTS=true
ACCENT_MODE=american
DATABASE_URL=sqlite:///agent_data.db
```

### Step 4: Deploy Ollama Service
Railway doesn't support GPU, so we use a separate Ollama service:

1. In Railway dashboard, click "New" → "Empty Service"
2. Name it "Ollama"
3. Add environment variable: `OLLAMA_ORIGINS=*`
4. Deploy
5. Copy the URL (e.g., `https://ollama-xxxx.railway.app`)
6. Update `OLLAMA_HOST` in your main service to this URL

### Step 5: Update Database Path
For persistent storage, use a PostgreSQL database:
1. Add Postgres addon in Railway
2. Update DATABASE_URL with the connection string

### Step 6: Verify Deployment
Visit your Railway URL and check:
- http://your-app.railway.app/health
- http://your-app.railway.app/docs

## Alternative: Render Deployment

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Deploy Web Service
1. Click "New+" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - Name: `voice-ai-agent`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Add environment variables (same as Railway)

### Step 3: Deploy Ollama
Render has similar limitations. Consider using:
- **Groq API** (free tier: 50k requests/month)
- **Together AI** (free credits)
- **Cloud Ollama hosting** services

Update `config.py` to use cloud API instead of local Ollama.

## Local Development Commands

```bash
# Start API server
python main.py

# Start Telegram bot
python bot.py

# Run with Docker
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

## Monitoring

- Logs: Railway/Render dashboards
- Health endpoint: `/health`
- API docs: `/docs`
