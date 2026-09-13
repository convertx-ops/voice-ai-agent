#!/usr/bin/env python3
"""Send final working URLs"""
import requests

BOT_TOKEN = "8835493193:AAHG7P4XPLxlahaxlSelVC_FNSs5N4NSMmY"
CHAT_ID = "7762840378"

message = """✅ <b>WEB URL NOW LIVE!</b> 🚀

<b>Direct Web Links:</b>

🌐 <b>LANDING PAGE:</b>
https://convertx-ops.github.io/voice-ai-agent.github.io/

🤖 <b>TELEGRAM BOT:</b>
https://t.me/VoiceAiCoach_bot

━━━━━━━━━━━━━━━━━━━
<b>Kya Milega:</b>
━━━━━━━━━━━━━━━━━━━

✅ Beautiful Landing Page
✅ All Features Explained
✅ Direct Telegram Bot Link
✅ Pricing Info
✅ One-Click Access

━━━━━━━━━━━━━━━━━━━
<b>Aj Ka Kaam:</b>
━━━━━━━━━━━━━━━━━━━

1️⃣ Chrome open karo
2️⃣ Upar diya URL paste karo
3️⃣ Landing page dikhega!
4️⃣ "Start Practicing" dabao
5️⃣ Telegram bot khulega
6️⃣ Share on social media!

━━━━━━━━━━━━━━━━━━━
<b>Free Features:</b>
━━━━━━━━━━━━━━━━━━━

• Interview Prep Mode
• Objection Handling Mode
• 10 conversations/day
• No credit card needed

<b>Premium (₹299/month):</b>
• Unlimited conversations
• BF/GF Chat + Custom Persona
• Advanced analytics

🎁 First 100 users = FREE Premium!

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
    print("✅ Live URLs sent to Telegram!")
    print(f"Message ID: {result['result']['message_id']}")
else:
    print(f"❌ Error: {result.get('description')}")
