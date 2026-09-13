#!/usr/bin/env python3
"""Send final launch message to Telegram"""
import requests

BOT_TOKEN = "8835493193:AAHG7P4XPLxlahaxlSelVC_FNSs5N4NSMmY"
CHAT_ID = "7762840378"

message = """🎉 <b>VOICE AI AGENT - LAUNCHED!</b> 🚀

<b>Direct Links (Chrome me kholo):</b>

🌐 <b>Landing Page:</b>
https://convertx-ops.github.io/voice-ai-agent.github.io/

💻 <b>GitHub Code:</b>
https://github.com/convertx-ops/voice-ai-agent

🤖 <b>Telegram Bot:</b>
https://t.me/VoiceAiCoach_bot

━━━━━━━━━━━━━━━━━━━
<b>Kya Build Hua:</b>
━━━━━━━━━━━━━━━━━━━

✅ Complete AI Voice Agent
✅ 4 Conversation Modes
✅ Ollama + Whisper + Edge TTS (100% Free)
✅ GitHub Repo Live
✅ Landing Page Live
✅ Message Bhej Diya

━━━━━━━━━━━━━━━━━━━
<b>Ab Kya Karein?</b>
━━━━━━━━━━━━━━━━━━━

1️⃣ Landing page URL Chrome me kholo
2️⃣ Telegram bot test karo
3️⃣ Social media pe share karo
4️⃣ Users lane shuru karo!

━━━━━━━━━━━━━━━━━━━
<b>Pricing:</b>
━━━━━━━━━━━━━━━━━━━

🆓 FREE: 10 conversations/day
💎 PREMIUM: ₹299/month (unlimited)

🎁 Launch Offer: First 100 users = FREE Premium!

━━━━━━━━━━━━━━━━━━━

— Rihan Pathan, Founder @ ConvertX Ops
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    'chat_id': CHAT_ID,
    'text': message,
    'parse_mode': 'HTML',
    'disable_web_page_preview': False
}

response = requests.post(url, json=payload, timeout=30)
result = response.json()

if result.get('ok'):
    print("✅ Message sent!")
    print(f"Message ID: {result['result']['message_id']}")
else:
    print(f"❌ Error: {result.get('description')}")
