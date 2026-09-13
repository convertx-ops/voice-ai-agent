# Voice AI Agent
AI-powered voice conversations for interview prep, objection handling, and more.

## Features
- 🎤 Real-time voice conversations via Telegram
- 🧠 Powered by Ollama (runs locally, free)
- 🗣️ Natural voice responses with Edge TTS
- 🎯 Multiple modes: Interview Prep, Objection Handling, BF/GF Chat
- 💰 Free tier available, premium features for unlimited use

## Tech Stack
- **Backend:** Python + FastAPI
- **AI:** Ollama (Qwen2.5)
- **Voice In:** Whisper (faster-whisper)
- **Voice Out:** Edge TTS (free, high quality)
- **Database:** SQLite
- **Bot Framework:** aiogram

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Ollama
Download from: https://ollama.com/download

### 3. Pull Model
```bash
ollama pull qwen2.5:3b
```

### 4. Configure
```bash
cp .env.example .env
# Edit .env with your Telegram bot token
```

### 5. Run
```bash
python main.py
```

For Telegram bot:
```bash
python bot.py
```

## Telegram Bot Setup
1. Message @BotFather on Telegram
2. Create new bot with `/newbot`
3. Copy the token
4. Add to `.env` file

## API Endpoints

### Health Check
```
GET /health
```

### Get Available Modes
```
GET /api/v1/modes
```

### Transcribe and Respond
```
POST /api/v1/transcribe
Content-Type: application/json

{
  "user_id": "user123",
  "mode": "interview",
  "audio_data": "<base64_encoded_audio>"
}
```

### Get Conversations
```
GET /api/v1/conversations/{user_id}
```

## Deployment

### Railway (Free Tier)
```bash
railway init
railway up
```

### Render (Free Tier)
Push to GitHub and connect to Render.

### Self-hosted
Run on any server with at least 4GB RAM.

## Premium Features
Unlocked with subscription:
- Unlimited conversations
- Custom personas
- Advanced analytics
- Priority support

## License
MIT
