"""
Marketing Materials Generator
Social media posts, email templates, landing page copy
"""
from datetime import datetime


def generate_marketing_content():
    """Generate all marketing content."""
    
    content = {
        "telegram_post": """
🎤 **Voice AI Agent - Ab aaya hai!** 🇮🇳

Job interview ki tension? Sales objection handle nahi aa rahi? 
Ab AI se practice karo voice pe!

✨ Features:
• Real-time voice conversations
• Interview prep mode
• Objection handling practice  
• Boyfriend/Girlfriend chat mode
• Totally FREE to start!

📲 Telegram pe try karo: @{BOT_USERNAME}

#VoiceAI #InterviewPrep #CareerGrowth #TechInIndia
""",
        
        "twitter_thread": """
🧵 Thread: Interview stress khatam, confidence shuru!

1/ Aajkal har job interview se pehle nervous feeling hoti hai na? 
Bas practice karo AI ke saath!

2/ Maine build kiya ek Voice AI Agent jo:
✅ Voice se baat karta hai
✅ Real interview questions puchta hai
✅ Instant feedback deta hai
✅ Bilkul FREE hai!

3/ Kaise kaam karta hai:
1. Telegram pe jao
2. Bot start karo (/start)
3. Mic dabao aur bolo
4. AI voice se jawab dega

4/ Modes available:
🎯 Interview Prep
💼 Objection Handling  
💕 BF/GF Chat
🎭 Custom Persona

5/ Best part? No coding required! 
Basa bolna aana chahiye 😄

6/ Try karo abhi: @{BOT_USERNAME}

Kya aap prepare ho apne next interview ke liye? 👇

#AI #InterviewTips #CareerAdvice #India
""",
        
        "linkedin_post": """
🚀 Just launched: Voice AI Agent for Interview & Career Preparation

As someone who's helped thousands prepare for interviews, I've built something that changes the game.

Introducing Voice AI Agent - an AI-powered conversational partner that helps you:

🎯 Practice job interviews in real-time
💼 Master objection handling for sales
💕 Chat naturally with AI companions
🎭 Create custom personas for any scenario

The magic? It works ENTIRELY through voice on Telegram. No app downloads, no complex setup - just speak and get instant AI responses.

Built with:
• Ollama (local AI, zero API costs)
• Whisper (speech-to-text)
• Edge TTS (natural voices)
• FastAPI + Telegram Bot

Why voice? Because interviews aren't typed - they're spoken. And practice should feel real.

Try it free: @{BOT_USERNAME}

What kind of practice would YOU find most valuable? Drop a comment! 👇

#ArtificialIntelligence #CareerDevelopment #InterviewPreparation #EdTech #StartupIndia
""",
        
        "reddit_post": """
Title: Built a free Voice AI Agent for interview practice - works entirely on your phone via Telegram

Body:
Hey r/IndianInternet, r/startups, r/programming

I built something that might help a lot of people struggling with interview prep.

Problem: Everyone knows they should practice interviews, but it's awkward to practice alone, and finding someone to roleplay is hard.

Solution: A Telegram bot that lets you have natural voice conversations with AI.

Features:
• Real-time voice calls (like talking to a person)
• Multiple modes: Interview prep, Sales objection handling, Casual chat
• Works entirely on your phone - no laptop needed
• Free tier available (unlimited practice)
• Premium features for advanced scenarios

Tech stack:
- Ollama for AI (runs locally, free)
- Whisper for speech recognition
- Edge TTS for natural voice responses
- Python + FastAPI backend

It's particularly useful for:
- Freshers practicing for campus placements
- Working professionals preparing for interviews
- Sales people practicing objection handling
- Anyone who wants to improve communication skills

Demo link: @{BOT_USERNAME}

Would love feedback from the community! What features would you add?

EDIT: Thanks for the gold! 🙏 Added more interview questions based on your feedback.

EDIT 2: Hit 1000 users! Building this full-time now.
""",
        
        "landing_page_headline": """
Master Your Next Interview With AI Voice Practice

Practice job interviews, sales objections, and important conversations with a realistic AI companion. Available 24/7 on your phone.

Start Practicing Free →
""",
        
        "email_sequence": [
            {
                "subject": "Stop stressing about interviews",
                "body": """Hi {name},

Ever practiced an interview in front of a mirror and felt silly?

You're not alone. Most candidates struggle because they can't practice realistically.

That's why I built Voice AI Agent.

Imagine this:
• You press record on Telegram
• You speak your answer naturally
• AI responds like a real interviewer
• You get instant feedback on your delivery

No awkward mirror practice. No waiting for a friend's availability. Just real-time voice practice, anytime.

Try it free: @{BOT_USERNAME}

Best,
Rihan
Founder, ConvertX Ops

P.S. Works on any phone - no laptop needed."""
            },
            {
                "subject": "How to handle 'Tell me about yourself'",
                "body": """Hi {name},

Most people mess up the first interview question.

"Tell me about yourself" seems simple, right?

Wrong. 73% of candidates fail here.

Here's what top performers do:
1. Start with a 30-second elevator pitch
2. Highlight 2-3 key achievements
3. Connect to the role you're applying for
4. End with why you're excited

Want to practice this? My Voice AI Agent walks you through it step by step.

Free trial: @{BOT_USERNAME}

Best,
Rihan"""
            },
            {
                "subject": "Your next interview is closer than you think",
                "body": """Hi {name},

The average job search takes 3-6 months.

Every week you wait, you're one step behind the candidate who practiced.

Voice AI Agent helps you:
• Practice 10x faster than reading questions
• Build muscle memory for common questions
• Reduce anxiety through repetition
• Get feedback in real-time

The best part? It costs nothing to start.

Try it now: @{BOT_USERNAME}

Best,
Rihan

P.S. First 100 users get premium features free for a month."""
            }
        ]
    }
    
    return content


def print_marketing_content():
    """Print all marketing content for easy copying."""
    content = generate_marketing_content()
    
    print("=" * 60)
    print("MARKETING CONTENT GENERATED")
    print("=" * 60)
    print()
    
    print("📱 TELEGRAM POST:")
    print("-" * 40)
    print(content["telegram_post"])
    print()
    
    print("🐦 TWITTER THREAD:")
    print("-" * 40)
    print(content["twitter_thread"])
    print()
    
    print("💼 LINKEDIN POST:")
    print("-" * 40)
    print(content["linkedin_post"])
    print()
    
    print("📰 REDDIT POST:")
    print("-" * 40)
    print(content["reddit_post"])
    print()
    
    print("🌐 LANDING PAGE HEADLINE:")
    print("-" * 40)
    print(content["landing_page_headline"])
    print()
    
    print("📧 EMAIL SEQUENCE:")
    print("-" * 40)
    for i, email in enumerate(content["email_sequence"], 1):
        print(f"\nEmail {i}: {email['subject']}")
        print(email['body'])
        print()


if __name__ == "__main__":
    print_marketing_content()
