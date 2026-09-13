"""
Telegram Bot Integration
Real-time voice conversations via Telegram
"""
import asyncio
import logging
import os
from datetime import datetime
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, PhotoSize, BufferedInputFile
from aiogram.enums import ParseMode
from aiogram.utils.exceptions import Unauthorized

from config import settings
from database import user_model, conversation_model, message_model
from agents import agent_engine
from voice import transcribe_audio, generate_speech

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceBot:
    def __init__(self):
        self.bot = Bot(token=settings.BOT_TOKEN)
        self.dp = Dispatcher()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Register all command handlers."""
        
        # Start command
        @self.dp.message(CommandStart())
        async def cmd_start(message: types.Message):
            """Handle /start command."""
            user = user_model.create_or_update(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            
            welcome_text = """
🎤 **Welcome to Voice AI Agent!**

Practice conversations with AI using just your voice!

**Available Modes:**
• 🎯 **Interview Prep** - Practice job interviews
• 💼 **Objection Handling** - Master sales objections
• 💕 **BF/GF Chat** - Casual conversational practice
• 🎭 **Custom Persona** - Create your own AI companion

**How to use:**
1. Send a voice message (tap the mic icon)
2. Speak naturally
3. Get instant voice response

**Commands:**
• /start - Start the bot
• /modes - See available modes
• /status - Check your subscription
• /help - Get help

Choose a mode and start speaking! 🚀
"""
            
            await message.answer(welcome_text, parse_mode=ParseMode.MARKDOWN)
        
        # Modes command
        @self.dp.message(Command("modes"))
        async def cmd_modes(message: types.Message):
            """List available conversation modes."""
            modes_text = """
**Available Conversation Modes:**

🎯 **Interview Prep** (FREE)
Practice job interviews with realistic scenarios
- HR screening calls
- Technical interviews
- Case studies
- Behavioral questions

💼 **Objection Handling** (FREE)
Master sales objections
- Price objections
- "Need to think about it"
- Competitor comparisons
- Gatekeepers

💕 **Boyfriend/Girlfriend Chat** (PREMIUM)
Natural conversational practice
- Daily check-ins
- Deep conversations
- Conflict resolution
- Emotional support

🎭 **Custom Persona** (PREMIUM)
Create any character you want
- Teacher/Mentor
- Friend/Companion
- Negotiator
- Any role

*Premium features unlock unlimited conversations and advanced personas!*
"""
            await message.answer(modes_text, parse_mode=ParseMode.MARKDOWN)
        
        # Status command
        @self.dp.message(Command("status"))
        async def cmd_status(message: types.Message):
            """Show user subscription status."""
            user = user_model.get_user(message.from_user.id)
            
            if not user:
                await message.answer("❌ User not found. Please restart with /start")
                return
            
            premium_status = "✅ Premium" if user['is_premium'] else "⚪ Free"
            
            status_text = f"""
**Account Status:**

👤 **User:** {user['first_name'] or 'Unknown'}
💎 **Plan:** {premium_status}
📅 **Member since:** {user['created_at']}

**Premium Benefits:**
• Unlimited conversations
• All conversation modes
• Custom personas
• Advanced feedback
• Priority support
"""
            await message.answer(status_text, parse_mode=ParseMode.MARKDOWN)
        
        # Help command
        @self.dp.message(Command("help"))
        async def cmd_help(message: types.Message):
            """Show help information."""
            help_text = """
**How to Use Voice AI Agent:**

1️⃣ **Select a Mode**
- Use /interview, /objection, /bf_gf commands
- Or just send a voice message (defaults to interview)

2️⃣ **Speak Naturally**
- Tap the microphone icon in Telegram
- Speak clearly in a quiet environment
- Wait for response after speaking

3️⃣ **Get Instant Feedback**
- AI responds with both text and voice
- Learn from mistakes in real-time
- Track your progress over time

**Tips for Best Results:**
• Speak clearly and at normal pace
• Use complete sentences
• Don't rush - pause between turns
• Practice regularly for improvement

Need more help? Just ask! 😊
"""
            await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)
        
        # Mode-specific commands
        @self.dp.message(Command("interview"))
        @self.dp.message(Command("objection"))
        @self.dp.message(Command("bf_gf"))
        async def cmd_set_mode(message: types.Message):
            """Set conversation mode."""
            command = message.command[0].replace('/', '')
            user_id = str(message.from_user.id)
            
            agent_engine.set_mode(user_id, command)
            
            mode_names = {
                "interview": "🎯 Interview Prep",
                "objection": "💼 Objection Handling",
                "bf_gf": "💕 BF/GF Chat"
            }
            
            await message.answer(
                f"✅ Switched to **{mode_names.get(command, command)}** mode!\n\n"
                f"Now send a voice message to start practicing.",
                parse_mode=ParseMode.MARKDOWN
            )
        
        # Handle voice messages
        @self.dp.message(types.ContentType.VOICE)
        async def handle_voice(message: types.Message):
            """Process voice messages and generate AI responses."""
            user_id = str(message.from_user.id)
            
            # Get current mode (default to interview)
            current_mode = agent_engine.current_mode.get(user_id, "interview")
            
            # Check if mode is premium
            from config import settings
            if current_mode in settings.PREMIUM_MODES:
                user = user_model.get_user(message.from_user.id)
                if user and not user['is_premium']:
                    await message.answer(
                        "🔒 This is a PREMIUM feature!\n\n"
                        "Upgrade to unlock unlimited conversations.\n"
                        "Contact @rihanpathan2425 for details.",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    return
            
            # Download voice message
            voice_file = await message.voice.get_file()
            voice_path = f"./temp_voice/{user_id}/{voice_file.file_path}"
            os.makedirs(os.path.dirname(voice_path), exist_ok=True)
            
            downloaded_file = await bot.download_file(voice_file.file_path, voice_path)
            
            # Read audio data
            with open(downloaded_file, 'rb') as f:
                audio_data = f.read()
            
            # Send typing indicator
            typing = await message.answer_chat_action(action="record_voice")
            
            try:
                # Step 1: Transcribe
                transcription = await transcribe_audio(audio_data)
                
                if not transcription or len(transcription.strip()) < 2:
                    await message.answer("I couldn't understand that. Could you speak more clearly?", 
                                       reply_to_message_id=message.message_id)
                    return
                
                # Step 2: Get AI response
                ai_response = await agent_engine.get_response(user_id, transcription)
                
                # Step 3: Send text response
                await message.answer(
                    f"🤖 **AI Response:**\n{ai_response}",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_to_message_id=message.message_id
                )
                
                # Step 4: Generate and send voice response
                audio_url = await generate_speech(ai_response, user_id, current_mode)
                
                if audio_url:
                    with open(audio_url, 'rb') as audio_file:
                        voice_content = BufferedInputFile(
                            audio_file.read(),
                            filename=f"response_{int(datetime.now().timestamp())}.ogg"
                        )
                        await message.answer_voice(
                            voice_content,
                            caption="🎙️ Voice Response",
                            reply_to_message_id=message.message_id
                        )
                
            except Exception as e:
                logger.error(f"Error processing voice: {e}")
                await message.answer(
                    "Sorry, I encountered an error. Please try again!",
                    reply_to_message_id=message.message_id
                )
            
            finally:
                # Cleanup
                if os.path.exists(downloaded_file):
                    os.remove(downloaded_file)
        
        # Handle text messages (fallback)
        @self.dp.message()
        async def handle_text(message: types.Message):
            """Handle text messages as fallback."""
            user_id = str(message.from_user.id)
            current_mode = agent_engine.current_mode.get(user_id, "interview")
            
            # Process through agent
            ai_response = await agent_engine.get_response(user_id, message.text)
            
            await message.answer(
                f"🤖 **AI:** {ai_response}",
                parse_mode=ParseMode.MARKDOWN
            )


# Create bot instance
bot = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher()


async def start_bot():
    """Start the Telegram bot."""
    logger.info("Starting Telegram bot...")
    
    # Set webhook (for production)
    # await bot.set_webhook(url=WEBHOOK_URL)
    
    # Start polling (for development)
    try:
        await dispatcher.start_polling(bot)
    except Unauthorized:
        logger.error("Invalid bot token. Check your BOT_TOKEN in .env file")
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start_bot())
