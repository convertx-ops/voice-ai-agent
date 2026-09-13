#!/usr/bin/env python3
"""Send final working URL to Telegram"""
import requests

BOT_TOKEN = "8835493193:AAHG7P4XPLxlahaxlSelVC_FNSs5N4NSMmY"
CHAT_ID = "7762840378"

message = """🎉 <b>WEB URL LIVE! (Finally Working)</b> 🚀

<b>Direct Links:</b>

🌐 <b>LANDING PAGE:</b>
https://convertx-ops.github.io/voice-ai-agent-web/

🤖 <b>TELEGRAM BOT:</b>
https://t.me/VoiceAiCoach_bot

━━━━━━━━━━━━━━━━━━━
<b>Test Now:</b>
━━━━━━━━━━━━━━━━━━━

1️⃣ Chrome open karo
2️⃣ Ye URL paste karo:
   convertx-ops.github.io/voice-ai-agent-web/
3️⃣ Beautiful landing page dikhega!
4️⃣ "Start Practicing Free" dabao
5️⃣ Telegram bot khulega!

━━━━━━━━━━━━━━━━━━━
<b>What You Get:</b>
━━━━━━━━━━━━━━━━━━━

✅ Beautiful Landing Page
✅ All Features Explained
✅ Direct Telegram Bot Link
✅ Pricing Info
✅ Mobile Responsive

━━━━━━━━━━━━━━━━━━━
<b>Features:</b>
━━━━━━━━━━━━━━━━━━━

🎯 Interview Prep (FREE)
💼 Objection Handling (FREE)
💕 BF/GF Chat (PREMIUM)
🎭 Custom Persona (PREMIUM)

Free: 10 conversations/day
Premium: ₹299/month (unlimited)

🎁 Launch Offer: First 100 users = FREE Premium!

━━━━━━━━━━━━━━━━━━━

— Rihan Pathan, Founder @ ConvertX Ops
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    'chat_id': CHAT_ID,
    'text': message,
    'parse_mode': 'HTML',
    'disable_web_page_preview': True
}

response = requests.post(url, json=payload, timeout=30)
result = response.json()

if result.get('ok'):
    print("✅ Final URL sent to Telegram!")
    print(f"Message ID: {result['result']['message_id']}")
else:
    print(f"❌ Error: {result.get('description')}")
