#!/usr/bin/env python3
"""
Send welcome message to Telegram user
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', '')
CHAT_ID = '7762840378'

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN not found in .env file")
    print("Please add your Telegram bot token to .env file")
    exit(1)

MESSAGE = """🎤 **Welcome to Voice AI Agent!** 🚀

Ab voice se practice karo — interview, sales, ya bas chat!

━━━━━━━━━━━━━━━━━━━
🔥 **Kya Kya Mil Raha Hai:**
━━━━━━━━━━━━━━━━━━━

🎯 **Interview Prep Mode** (FREE)
• Real-time voice interview practice
• HR screening simulation
• Technical + Behavioral questions
• Instant feedback after every answer
• Perfect for campus placements & job switches

💼 **Objection Handling Mode** (FREE)
• Sales objections practice
• "Too expensive" handled karna seekho
• "Need to think about it" ka response
• Real customer roleplay
• LAER & Feel-Felt-Found frameworks

💕 **Boyfriend/Girlfriend Chat** (PREMIUM)
• Natural conversational practice
• Daily check-ins simulate karo
• Emotional intelligence build karo
• Conflict resolution practice

🎭 **Custom Persona** (PREMIUM)
• Teacher, mentor, negotiator — jo chahe banao
• apni personality customize karo
• Koi bhi scenario practice karo

━━━━━━━━━━━━━━━━━━━
✨ **Best Features:**
━━━━━━━━━━━━━━━━━━━

✅ Bilkul FREE start kar sakte ho
✅ Telegram pe kaam karta hai — app download nahi chahiye
✅ Mobile se voice messages bhejo, voice reply pao
✅ Real-time conversations (typing nahi!)
✅ Ollama + Whisper + Edge TTS — sab free tech stack
✅ ₹0 running cost (apne laptop pe run karo)

━━━━━━━━━━━━━━━━━━━
📱 **Kaise Use Karein:**
━━━━━━━━━━━━━━━━━━━

1️⃣ Telegram open karo
2️⃣ Search: @VoiceAiCoach_bot
3️⃣ Start dabao (/start)
4️⃣ Mic button daba ke bolo!
5️⃣ AI voice se jawab dega

Commands:
• /interview — Interview mode
• /objection — Objection handling  
• /bf_gf — BF/GF chat (premium)
• /custom — Custom persona (premium)
• /status — Apna plan check karo
• /help — Madad chahiye?

━━━━━━━━━━━━━━━━━━━
💰 **Pricing:**
━━━━━━━━━━━━━━━━━━━

🆓 FREE Tier:
• 10 conversations/day
• Interview + Objection modes
• Standard voice quality

💎 PREMIUM (₹299/month):
• Unlimited conversations
• BF/GF Chat unlock
• Custom Personas
• Advanced analytics
• Priority support

━━━━━━━━━━━━━━━━━━━
🎁 **Launch Offer:**
━━━━━━━━━━━━━━━━━━━

First 100 users ko PREMIUM FREE for 1 month!
Refer 3 friends → Lifetime premium free!

━━━━━━━━━━━━━━━━━━━
🚀 **Ready to Start?**
━━━━━━━━━━━━━━━━━━━

Abhi test karo: Telegram pe jaake @VoiceAiCoach_bot ko message karo!

Questions? Reply karo yahan. 💬

— Rihan Pathan, Founder @ ConvertX Ops
"""

def send_telegram_message(token, chat_id, message):
    """Send message to Telegram user"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        result = response.json()
        
        if result.get('ok'):
            print("✅ Message sent successfully!")
            print(f"Message ID: {result.get('result', {}).get('message_id')}")
            return True
        else:
            print("❌ Failed to send message:")
            print(f"Error: {result.get('description')}")
            return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

if __name__ == "__main__":
    print("📤 Sending welcome message to Telegram...")
    print(f"Chat ID: {CHAT_ID}")
    print(f"Bot: @VoiceAiCoach_bot")
    print()
    
    success = send_telegram_message(BOT_TOKEN, CHAT_ID, MESSAGE)
    
    if success:
        print("\n✅ Done! User will receive the message shortly.")
    else:
        print("\n⚠️  Make sure BOT_TOKEN is correct in .env file")
