#!/usr/bin/env python3
"""
Simple script to send welcome message to Telegram user
Usage: python send_message.py BOT_TOKEN
"""
import sys
import requests

def send_message(bot_token, chat_id, message_text):
    """Send message via Telegram Bot API"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        'parse_mode': 'Markdown',
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

# Message content
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

GitHub Repo: https://github.com/convertx-ops/voice-ai-agent
Bot: @VoiceAiCoach_bot

Abhi test karo aur share karo! 💬

— Rihan Pathan, Founder @ ConvertX Ops
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python send_message.py BOT_TOKEN")
        print("")
        print("Step 1: Open Telegram")
        print("Step 2: Search @BotFather")
        print("Step 3: Send /newbot (agar naya bot banana ho)")
        print("Step 4: Copy the HTTP API token")
        print("Step 5: Run this command with token:")
        print("   python send_message.py YOUR_BOT_TOKEN_HERE")
        print("")
        print("Or just manually send the message below to:")
        print(f"Telegram ID: 7762840378")
        sys.exit(1)
    
    bot_token = sys.argv[1]
    chat_id = "7762840378"
    
    print("📤 Sending message to Telegram...")
    print(f"Recipient: {chat_id}")
    print(f"Bot: @VoiceAiCoach_bot")
    print("")
    
    success = send_message(bot_token, chat_id, MESSAGE)
    
    if success:
        print("\n✅ Done! Check your Telegram.")
    else:
        print("\n⚠️  Failed. Make sure token is correct.")
        print("Get new token from @BotFather")
