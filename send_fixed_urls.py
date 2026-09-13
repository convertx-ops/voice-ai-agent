#!/usr/bin/env python3
"""Send corrected live URLs to Telegram"""
import requests

BOT_TOKEN = "8835493193:AAHG7P4XPLxlahaxlSelVC_FNSs5N4NSMmY"
CHAT_ID = "7762840378"

message = """🔄 <b>LIVE URL FIXED!</b> ✅

<b>Direct Links (Chrome Me Kholo):</b>

🌐 <b>Landing Page (NOW WORKING):</b>
https://convertx-ops.github.io/voice-ai-agent.github.io/

🤖 <b>Telegram Bot:</b>
https://t.me/VoiceAiCoach_bot

━━━━━━━━━━━━━━━━━━━
<b>Quick Test:</b>
━━━━━━━━━━━━━━━━━━━

1️⃣ Chrome open karo
2️⃣ Ye URL paste karo:
   convertx-ops.github.io/voice-ai-agent.github.io/
3️⃣ Landing page dikhega!
4️⃣ "Start Practicing Free" button dabao
5️⃣ Telegram bot khulega!

━━━━━━━━━━━━━━━━━━━

— Rihan Pathan, Founder @ ConvertX Ops
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    'chat_id': CHAT_ID,
    'text': message,
    'parse_mode': 'HTML'
}

response = requests.post(url, json=payload, timeout=30)
result = response.json()

if result.get('ok'):
    print("✅ Fixed URLs sent!")
    print(f"Message ID: {result['result']['message_id']}")
else:
    print(f"❌ Error: {result.get('description')}")
