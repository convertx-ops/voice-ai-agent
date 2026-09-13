#!/usr/bin/env python3
"""Send marketing messages to different platforms"""
import requests
import time

BOT_TOKEN = "8835493193:AAHG7P4XPLxlahaxlSelVC_FNSs5N4NSMmY"
CHAT_ID = "7762840378"

# Message 1: Features Overview
features_msg = """🎤 <b>VOICE AI AGENT - FEATURES</b>

<b>4 Conversation Modes:</b>

🎯 <b>Interview Prep (FREE)</b>
• Real-time voice interviews
• HR screening simulation
• Technical + behavioral questions
• Instant feedback
• Perfect for placements

💼 <b>Objection Handling (FREE)</b>
• Sales objection practice
• "Too expensive" responses
• "Need to think" handling
• LAER framework
• Real customer roleplay

💕 <b>BF/GF Chat (PREMIUM)</b>
• Natural conversation practice
• Daily check-ins
• Emotional intelligence
• Conflict resolution

🎭 <b>Custom Persona (PREMIUM)</b>
• Teacher, mentor, negotiator
• Any character you imagine
• Fully customizable
• Unlimited scenarios

<b>How It Works:</b>
1. Open Telegram → @VoiceAiCoach_bot
2. Press /start
3. Choose mode
4. Speak via mic
5. Get voice response!

Link: https://t.me/VoiceAiCoach_bot
"""

# Message 2: Technical Details
tech_msg = """⚙️ <b>TECH STACK (100% FREE)</b>

<b>Backend:</b> Python + FastAPI
<b>AI Brain:</b> Ollama Qwen2.5 (local)
<b>Voice In:</b> Whisper STT
<b>Voice Out:</b> Edge TTS
<b>Database:</b> SQLite
<b>Hosting:</b> Your laptop / Railway free tier

<b>Total Cost: ₹0/month</b>

<b>Features:</b>
✅ Real-time voice conversations
✅ Works on any smartphone
✅ No app download needed
✅ Unlimited local processing
✅ Private & secure

GitHub: https://github.com/convertx-ops/voice-ai-agent
"""

# Message 3: Business Model
business_msg = """💰 <b>BUSINESS MODEL</b>

<b>Free Tier:</b>
• 10 conversations/day
• Interview + Objection modes
• Standard voice quality
• Perfect for testing

<b>Premium Tier: ₹299/month</b>
• Unlimited conversations
• All modes unlocked
• Custom personas
• Advanced analytics
• Priority support

<b>Revenue Projection:</b>
• 100 users × 5% = 5 premium = ₹1,495/mo
• 1,000 users × 5% = 50 premium = ₹14,950/mo
• 10,000 users = ₹1,49,500/mo

<b>Launch Offer:</b>
First 100 users get PREMIUM FREE for 1 month!
Refer 3 friends = Lifetime premium free!
"""

# Message 4: Marketing Copy
marketing_msg = """📣 <b>PROMPT FOR SOCIAL MEDIA</b>

<b>LinkedIn Post:</b>
"🚀 Just launched Voice AI Agent - an AI-powered voice coach for interview prep, sales objections, and conversation practice. Works entirely on Telegram! Built with Ollama + Whisper + Edge TTS - 100% free stack. Try it: https://t.me/VoiceAiCoach_bot"

<b>Twitter Thread:</b>
"🧵 I built a Voice AI Agent that helps you practice interviews - and it's FREE

Most people can't practice interviews because:
- Finding someone to roleplay is hard
- Recording yourself feels awkward
- Getting feedback takes time

So I built: A Telegram bot that listens to your voice and responds with voice. No app download needed.

Built 100% free with Ollama + Whisper + Edge TTS.

Try it: https://t.me/VoiceAiCoach_bot"

<b>Reddit Post:</b>
"Built a free Voice AI Agent for interview practice - works entirely on Telegram. No app download, just voice messages. Tech: Ollama + Whisper + Edge TTS. All free. Link: https://t.me/VoiceAiCoach_bot"

<b>Instagram Reel Script:</b>
"Stop scrolling. This could get you your dream job. [Show Telegram bot] This is Voice AI Agent. Practice interviews with AI voice. No app download needed. Link in bio."
"""

messages = [features_msg, tech_msg, business_msg, marketing_msg]

for i, msg in enumerate(messages, 1):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': msg,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(url, json=payload, timeout=30)
    result = response.json()
    
    if result.get('ok'):
        print(f"✅ Message {i} sent!")
        time.sleep(1)
    else:
        print(f"❌ Message {i} failed: {result.get('description')}")

print("\n🎉 All marketing messages sent!")
