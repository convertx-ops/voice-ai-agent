#!/usr/bin/env python3
"""Send final correct URL to Telegram"""
import requests

BOT_TOKEN = "8835493193:AAHG7P4XPLxlahaxlSelVC_FNSs5N4NSMmY"
CHAT_ID = "7762840378"

message = """🎊 <b>FINALLY LIVE! WEB URL WORKING!</b> 🎊

<b>YOUR DIRECT WEB LINK:</b>

🌐 https://convertx-ops.github.io/voice-ai-agent-web/

━━━━━━━━━━━━━━━━━━━
<b>YE URL KHOLKE DEKHO:</b>
━━━━━━━━━━━━━━━━━━━

✅ Beautiful landing page dikhega
✅ Features explain honge
✅ Direct Telegram bot link
✅ Pricing information
✅ Mobile friendly design

━━━━━━━━━━━━━━━━━━━
<b>Telegram Bot:</b>
━━━━━━━━━━━━━━━━━━━

https://t.me/VoiceAiCoach_bot
(Bot already working!)

━━━━━━━━━━━━━━━━━━━
<b>Quick Actions:</b>
━━━━━━━━━━━━━━━━━━━

1️⃣ Chrome kholo
2️⃣ Ye URL paste karo:
   convertx-ops.github.io/voice-ai-agent-web/
3️⃣ Landing page enjoy karo!
4️⃣ "Start Practicing" dabao
5️⃣ Telegram bot khulega!

━━━━━━━━━━━━━━━━━━━
<b>Features Available:</b>
━━━━━━━━━━━━━━━━━━━

🎯 Interview Prep (FREE)
💼 Objection Handling (FREE)
💕 BF/GF Chat (PREMIUM - ₹299/month)
🎭 Custom Persona (PREMIUM)

🎁 LAUNCH OFFER: First 100 users get FREE Premium!

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
    print("✅ LIVE URL sent to Telegram!")
    print(f"Message ID: {result['result']['message_id']}")
else:
    print(f"❌ Error: {result.get('description')}")
