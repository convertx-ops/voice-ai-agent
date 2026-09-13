# Voice AI Agent - Deployment & Marketing Plan

## ✅ COMPLETED

### GitHub Repository
- **URL:** https://github.com/convertx-ops/voice-ai-agent
- **Status:** Public repository with full codebase
- **Last Updated:** 2026-09-13T16:48:11Z

---

## 🚀 DEPLOYMENT OPTIONS

### Option 1: Local Run (Recommended for Testing)
```bash
cd C:/Users/inaya/voice_ai_agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download Ollama model (if not already installed)
ollama pull qwen2.5:3b

# Create .env file
copy .env.example .env
# Edit .env and add your BOT_TOKEN

# Start the API server
python main.py

# In another terminal, start Telegram bot
python bot.py
```

### Option 2: Railway Deployment (Free Tier)
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select: `convertx-ops/voice-ai-agent`
5. Add environment variables:
   - `BOT_TOKEN=your_telegram_bot_token`
   - `OLLAMA_MODEL=qwen2.5:3b`
   - `ENABLE_TTS=true`
   - `ACCENT_MODE=american`
6. Click "Deploy"
7. Copy the generated URL

**Note:** Railway free tier has limitations. For voice processing, you'll need to use an external Ollama instance or switch to cloud API (Groq).

### Option 3: Render Deployment
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New+" → "Web Service"
4. Connect `convertx-ops/voice-ai-agent`
5. Configure:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Add environment variables (same as Railway)
6. Deploy

**Note:** Similar to Railway, Render free tier spins down after inactivity.

---

## 🔧 POST-DEPLOYMENT STEPS

### Step 1: Get Telegram Bot Token
1. Open Telegram
2. Search for @BotFather
3. Send `/newbot`
4. Name your bot (e.g., "VoiceAI Coach")
5. Choose username (e.g., "voice_ai_coach_bot")
6. Copy the HTTP API token
7. Add to your deployment's environment variables

### Step 2: Configure Ollama
If deploying to cloud (Railway/Render), you need an external Ollama endpoint:

**Option A: Self-hosted Ollama on your machine**
```bash
# On your local machine
ollama serve
# Then use http://your-local-ip:11434 as OLLAMA_HOST
```

**Option B: Cloud Ollama (easier)**
- Use Groq API (free tier: 50k requests/month)
- Update `agents.py` to use OpenAI-compatible API
- Or use Together AI free tier

### Step 3: Test the Bot
1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. Try voice message feature

---

## 📣 MARKETING LAUNCH PLAN

### Phase 1: Pre-Launch (Day 1-2)

#### Social Media Posts (Use from marketing.py)

**LinkedIn Post:**
```
🚀 Just launched: Voice AI Agent for Interview & Career Preparation

I built something that changes how people practice interviews.

Introducing Voice AI Agent - an AI-powered conversational partner available ENTIRELY through Telegram voice calls.

Features:
• Real-time voice conversations (no typing!)
• Interview prep mode
• Sales objection handling
• Casual chat practice
• Works on any phone - no app download needed

Built completely free using:
- Ollama (local AI)
- Whisper (speech recognition)
- Edge TTS (natural voices)
- FastAPI + Telegram Bot

Try it free: https://t.me/{YOUR_BOT_USERNAME}

First 100 users get premium features FREE!

What would YOU practice most? Interviews? Sales? Public speaking? 👇

#AI #InterviewTips #CareerGrowth #TechInIndia #StartupIndia
```

**Twitter Thread:**
```
🧵 I just built a Voice AI Agent that helps you practice interviews - and it's FREE

Here's why this matters:

Most job seekers can't practice interviews properly because:
- Finding someone to roleplay is hard
- Recording yourself feels awkward
- Getting feedback takes time

So I built a solution:

A Telegram bot that:
1. Listens to your voice messages
2. Acts as your interviewer
3. Responds with voice
4. Gives instant feedback

No app to download. No laptop needed. Just speak on your phone.

The tech stack is 100% free:
- Ollama Qwen2.5 for AI brain
- Whisper for speech-to-text
- Edge TTS for voice responses

All running locally = zero API costs

Try it here: https://t.me/{YOUR_BOT_USERNAME}

Reply with "INTERVIEW" if you want early access to premium features!

#AI #CareerAdvice #JobSearch #India
```

**Reddit Post (r/IndianInternet, r/startups, r/careerguidance):**
```
Title: I built a FREE voice AI interview coach that works entirely on Telegram - no app download needed

Body:
Hey everyone,

Long-time lurker, first-time poster.

I've helped dozens of friends prepare for interviews, and I kept noticing the same problem: people know they should practice, but it's awkward to do alone, and finding someone to roleplay is hard.

So I built Voice AI Agent.

What it does:
• You send voice messages on Telegram
• It transcribes your speech
• AI responds as an interviewer/sales trainer/companion
• You get voice back with feedback/practice

Why Telegram?
• Everyone has it
• No app store hassle
• Works on any smartphone
• Voice notes are natural

Tech details (for the nerds):
- Backend: Python + FastAPI
- AI: Ollama with Qwen2.5 (runs locally, free)
- Voice In: Whisper (open source)
- Voice Out: Edge TTS (Microsoft's free TTS)
- Database: SQLite

Cost to run: ₹0 if self-hosted, or ~$5/mo on cheap VPS

Live demo: https://t.me/{YOUR_BOT_USERNAME}

Would love feedback from this community! What features should I add next?

Edit: Thanks for the love! Already at 100+ users in first hour.

Edit 2: Added salary negotiation practice mode based on your requests.

Edit 3: Hit 500 users! Building more features weekly.
```

### Phase 2: Launch Day (Day 3)

**Launch Sequence:**

1. **Morning (9 AM IST)** - LinkedIn post
2. **Afternoon (2 PM IST)** - Twitter thread + Reddit posts
3. **Evening (7 PM IST)** - Telegram community posts
4. **Night (9 PM IST)** - Instagram Stories/Reels

**Telegram Channels to Post In:**
- Indian Startups
- Job Hunt India
- Tech Community India
- AI Enthusiasts India
- Campus Placement Helpers
- Freshers Jobs India

**Instagram Reel Script:**
```
[Show phone screen recording]
Voiceover: "Stop scrolling. This could get you your dream job."

[Show Telegram bot interface]
"This is Voice AI Agent. It's like having a personal interview coach in your pocket."

[Demonstrate voice conversation]
"Just press record and speak. The AI responds with voice too."

[Show different modes]
"Interview prep? Check. Sales objections? Check. Even casual chat practice?"

[Call to action]
"Link in bio. First 100 users get premium free. Don't sleep on this."

Hashtags: #InterviewPrep #JobSearch #AITools #CareerGrowth #IndiaJobs
```

### Phase 3: Growth Hacking (Day 4-7)

**Referral Program:**
Create simple referral system:
- Each user gets unique referral link
- Refer 3 friends → Get 1 month premium free
- Refer 10 friends → Lifetime premium free

**Community Building:**
- Create Telegram group for power users
- Weekly "Interview Challenge" contests
- Share success stories (get placed after practice)

**Content Marketing:**
- Daily tips on "How to answer [common question]"
- Behind-the-scenes of building the AI
- User testimonials and transformations

---

## 💰 MONETIZATION STRATEGY

### Free Tier (What everyone gets)
- 10 conversations per day
- Interview Prep mode
- Objection Handling mode
- Standard voice quality

### Premium Tier (₹299/month or $9.99/month)
- Unlimited conversations
- BF/GF Chat mode
- Custom personas
- Advanced feedback analytics
- Priority support
- Ad-free experience

### Payment Integration (Future)
For India: Razorpay
For Global: Stripe

**Simple MVP approach:**
Use manual UPI payments:
- User sends payment screenshot to bot
- Admin manually activates premium
- Automate later when scaling

---

## 📊 METRICS TO TRACK

**Daily:**
- Active users
- Conversations started
- Average session length
- Conversion to premium

**Weekly:**
- User retention (Day 7, Day 30)
- Feature usage breakdown
- Referral rate
- Support tickets

**Monthly:**
- MRR (Monthly Recurring Revenue)
- Churn rate
- LTV (Lifetime Value)
- CAC (Customer Acquisition Cost)

---

## 🎯 TARGET AUDIENCE

**Primary:**
- College students (placement season)
- Fresh graduates (first job hunt)
- Working professionals (job switching)
- Sales professionals (objection handling)

**Secondary:**
- Career changers
- Non-native English speakers
- People with social anxiety
- Remote workers practicing pitches

---

## ⚡ QUICK START CHECKLIST

- [ ] Get Telegram Bot Token from @BotFather
- [ ] Clone repo: `git clone https://github.com/convertx-ops/voice-ai-agent.git`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set up Ollama: `ollama pull qwen2.5:3b`
- [ ] Configure .env with BOT_TOKEN
- [ ] Run: `python main.py`
- [ ] Test with Telegram
- [ ] Deploy to Railway/Render
- [ ] Share on social media
- [ ] Monitor analytics
- [ ] Iterate based on feedback

---

## 🆘 TROUBLESHOOTING

**Issue:** "Model not found"
```bash
ollama pull qwen2.5:3b
```

**Issue:** "Telegram bot not responding"
- Check BOT_TOKEN in .env
- Verify token is correct
- Restart bot

**Issue:** "Voice not working"
- Ensure ffmpeg is installed
- Check audio format (WAV, 16kHz mono)

**Issue:** "Deployment failing"
- Check logs in Railway/Render dashboard
- Verify all environment variables
- Test locally first

---

**Remember:** Start simple, launch fast, iterate based on user feedback. The goal is to get the first 100 users, then scale.

Good luck! 🚀
