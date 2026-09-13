# Voice AI Agent - Complete Setup Guide

## ✅ What Has Been Built

A complete Voice AI Agent system with:
- **FastAPI Backend** - REST API for voice processing
- **Telegram Bot** - Real-time voice conversations
- **Ollama Integration** - Local AI (Qwen2.5) running free
- **Whisper STT** - Speech-to-text (runs locally)
- **Edge TTS** - Text-to-speech with natural voices
- **SQLite Database** - Stores conversations and users
- **Marketing Materials** - Social media posts ready to use

## 🚀 Quick Start (3 Steps)

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `voice-ai-agent`
3. Make it **Public**
4. Click "Create repository"

### Step 2: Push Code
Run these commands in your terminal:

```bash
cd C:/Users/inaya/voice_ai_agent

# Authenticate with GitHub (do this once)
gh auth login

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/voice-ai-agent.git
git push -u origin main
```

### Step 3: Deploy
Follow the guide in `DEPLOYMENT.md` for Railway/Render setup.

---

## 📁 Project Structure

```
voice_ai_agent/
├── main.py              # FastAPI server
├── bot.py               # Telegram bot
├── agents.py            # AI agent logic (interview/objection/bf_gf)
├── voice.py             # Whisper + Edge TTS integration
├── database.py          # SQLite database models
├── config.py            # Configuration
├── marketing.py         # Marketing content generator
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container deployment
├── docker-compose.yml   # Docker orchestration
├── deploy.sh            # Linux/Mac deployment script
├── deploy_windows.bat   # Windows deployment script
├── .env.example         # Environment template
└── README.md            # Documentation
```

---

## 🔑 What You Need to Get Started

1. **Telegram Bot Token** (5 minutes)
   - Message @BotFather on Telegram
   - Send `/newbot`
   - Follow instructions
   - Copy the token

2. **Install Ollama** (2 minutes)
   - Download from https://ollama.com/download
   - Run: `ollama pull qwen2.5:3b`

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure**
   ```bash
   cp .env.example .env
   # Edit .env and add your BOT_TOKEN
   ```

5. **Run**
   ```bash
   python main.py      # Start API server
   python bot.py       # Start Telegram bot
   ```

---

## 💰 Monetization Strategy

### Free Tier (What everyone gets)
- Interview Prep mode
- Objection Handling mode
- 10 conversations per day
- Standard voice quality

### Premium Tier (₹299/month or $9.99/month)
- Unlimited conversations
- BF/GF Chat mode
- Custom personas
- Advanced feedback analytics
- Priority support

---

## 🎯 Marketing Plan (Already Written)

All marketing materials are in `marketing.py`:

- **Telegram Post** - Launch announcement
- **Twitter Thread** - Viral thread format
- **LinkedIn Post** - Professional audience
- **Reddit Post** - r/IndianInternet, r/startups
- **Landing Page Headline** - Conversion optimized
- **Email Sequence** - 3-part nurture sequence

To generate and print all marketing content:
```bash
python marketing.py
```

---

## 📱 How It Works (User Flow)

1. User opens Telegram
2. Searches for your bot (@YourBotName)
3. Types `/start`
4. Chooses mode: `/interview`, `/objection`, or `/bf_gf`
5. Presses mic button and speaks
6. AI transcribes → thinks → responds with voice
7. User gets instant feedback/practice

---

## 🛠️ Tech Stack (All Free)

| Component | Tool | Cost |
|-----------|------|------|
| AI Brain | Ollama (Qwen2.5) | FREE |
| Speech-to-Text | Whisper | FREE |
| Text-to-Speech | Edge TTS | FREE |
| Backend | FastAPI | FREE |
| Database | SQLite | FREE |
| Hosting | Your laptop / Railway free tier | ₹0-5/mo |
| Bot Platform | Telegram | FREE |

**Total Monthly Cost: ₹0 to start**

---

## 🔒 Security Notes

- All voice data stays local (no third-party APIs except Edge TTS)
- SQLite database stored locally
- No payment processing in MVP (use manual UPI/PayPal links)
- Rate limiting via Telegram's own limits

---

## 📈 Growth Path

1. **Launch Phase** (Week 1-2)
   - Share on all social media
   - Post in Indian tech/career communities
   - Offer free premium for first 100 users

2. **Growth Phase** (Week 3-4)
   - Collect testimonials
   - Add more interview questions
   - Introduce referral program

3. **Monetization Phase** (Month 2+)
   - Launch premium tier
   - Add payment integration (Razorpay for India)
   - Expand to more languages

---

## 🆘 Troubleshooting

### Issue: "Ollama not found"
**Solution:** Install Ollama from https://ollama.com/download

### Issue: "Model not loaded"
**Solution:** Run `ollama pull qwen2.5:3b`

### Issue: "Telegram bot not responding"
**Solution:** Check BOT_TOKEN in .env file

### Issue: "Voice not working"
**Solution:** Ensure ffmpeg is installed (required by Whisper)

---

## 📞 Support

For help or customizations:
- Email: rihanpathan2425@gmail.com
- Telegram: @rihanpathan2425

---

**Built with ❤️ for Gen Z and Alpha who want to succeed without spending money.**
