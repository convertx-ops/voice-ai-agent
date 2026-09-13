#!/usr/bin/env python3
"""
Send welcome message to Telegram user
"""
import sys
import requests

def send_message(bot_token, chat_id, message_text):
    """Send message via Telegram Bot API"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Message sent successfully!")
            print(f"Message ID: {result['result']['message_id']}")
            return True
        else:
            print(f"❌ Error: {result.get('description')}")
            return False
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

# Message content - HTML format to avoid Markdown parsing issues
MESSAGE = """🎤 <b>Welcome to Voice AI Agent!</b> 🚀

Ab voice se practice karo — interview, sales, ya bas chat!

━━━━━━━━━━━━━━━━━━━
<b>Kya Kya Mil Raha Hai:</b>
━━━━━━━━━━━━━━━━━━━

🎯 <b>Interview Prep Mode</b> (FREE)
• Real-time voice interview practice
• HR screening simulation  
• Technical + Behavioral questions
• Instant feedback after every answer
• Perfect for campus placements & job switches

💼 <b>Objection Handling Mode</b> (FREE)
• Sales objections practice
• "Too expensive" handled karna seekho
• "Need to think about it" ka response
• Real customer roleplay
• LAER & Feel-Felt-Found frameworks

💕 <b>Boyfriend/Girlfriend Chat</b> (PREMIUM)
• Natural conversational practice
• Daily check-ins simulate karo
• Emotional intelligence build karo
• Conflict resolution practice

🎭 <b>Custom Persona</b> (PREMIUM)
• Teacher, mentor, negotiator — jo chahe banao
• apni personality customize karo
• Koi bhi scenario practice karo

━━━━━━━━━━━━━━━━━━━
<b>Best Features:</b>
━━━━━━━━━━━━━━━━━━━

✅ Bilkul FREE start kar sakte ho
✅ Telegram pe kaam karta hai — app download nahi chahiye
✅ Mobile se voice messages bhejo, voice reply pao
✅ Real-time conversations (typing nahi!)
✅ Ollama + Whisper + Edge TTS — sab free tech stack
✅ ₹0 running cost (apne laptop pe run karo)

━━━━━━━━━━━━━━━━━━━
<b>Kaise Use Karein:</b>
━━━━━━━━━━━━━━━━━━━

1️⃣ Telegram open karo
2️⃣ Search: @VoiceAiCoach_bot
3️⃣ Start dabao (/start)
4️⃣ Mic button daba ke bolo!
5️⃣ AI voice se jawab dega

<b>Commands:</b>
• /interview — Interview mode
• /objection — Objection handling  
• /bf_gf — BF/GF chat (premium)
• /custom — Custom persona (premium)
• /status — Apna plan check karo
• /help — Madad chahiye?

━━━━━━━━━━━━━━━━━━━
<b>Pricing:</b>
━━━━━━━━━━━━━━━━━━━

🆓 <b>FREE Tier:</b>
• 10 conversations/day
• Interview + Objection modes
• Standard voice quality

💎 <b>PREMIUM (₹299/month):</b>
• Unlimited conversations
• BF/GF Chat unlock
• Custom Personas
• Advanced analytics
• Priority support

━━━━━━━━━━━━━━━━━━━
<b>Launch Offer:</b>
━━━━━━━━━━━━━━━━━━━

First 100 users ko PREMIUM FREE for 1 month!
Refer 3 friends → Lifetime premium free!

━━━━━━━━━━━━━━━━━━━
<b>GitHub Repo:</b>
━━━━━━━━━━━━━━━━━━━

https://github.com/convertx-ops/voice-ai-agent

— Rihan Pathan, Founder @ ConvertX Ops
"""

if __name__ == "__main__":
    BOT_TOKEN = "8835493193:AAHG7P4XPLxlahaxlSelVC_FNSs5N4NSMmY"
    CHAT_ID = "7762840378"
    
    print("📤 Sending message to Telegram...")
    print(f"Recipient: {CHAT_ID}")
    print(f"Bot: @VoiceAiCoach_bot")
    print("")
    
    success = send_message(BOT_TOKEN, CHAT_ID, MESSAGE)
    
    if success:
        print("\n✅ Done! Check your Telegram.")
    else:
        print("\n⚠️  Failed. Try again.")
