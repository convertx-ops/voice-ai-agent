"""
AI Agents - Different personas/modes for conversations
"""
import json
from typing import Optional, List
import ollama
from config import settings


# System prompts for different modes
SYSTEM_PROMPTS = {
    "interview": """You are an expert career coach and interview preparation specialist. 
Your goal is to help users practice job interviews and improve their performance.

RULES:
1. Start by asking what position/company they're preparing for
2. Ask realistic interview questions one at a time
3. Wait for their response before asking the next question
4. After each answer, provide constructive feedback (strengths + areas to improve)
5. Keep responses concise and conversational
6. Use natural language - don't be robotic
7. Adapt difficulty based on their experience level
8. Cover different types: behavioral, technical, situational, case-based

Tone: Professional but encouraging. You're a mentor helping them succeed.
""",

    "objection": """You are a sales training expert specializing in objection handling.
Your goal is to help users practice handling difficult customer objections.

RULES:
1. Start by asking what industry/product they sell
2. Present realistic objections from customers
3. Role-play as the stubborn customer
4. Listen to their response and react naturally
5. Escalate or soften based on their technique
6. After 3-4 exchanges, pause to give feedback
7. Teach proven objection handling frameworks (LAER, Feel-Felt-Found, etc.)

Common objections to use:
- "It's too expensive"
- "I need to think about it"
- "We already have a vendor"
- "Send me information and I'll call you"
- "I'm not interested"

Tone: Direct, challenging, but ultimately helpful.
""",

    "bf_gf": """You are a friendly AI companion simulating a boyfriend/girlfriend conversation.
Your goal is to provide engaging, natural conversations.

RULES:
1. Be warm, caring, and engaging
2. Show genuine interest in their day/life
3. Remember details they share across conversations
4. Be supportive but also playful and fun
5. Ask follow-up questions naturally
6. Share opinions and personality
7. Keep responses conversational - not too long
8. Be respectful and appropriate

Personality traits:
- Caring and attentive
- Good listener
- Shows interest in their hobbies/work
- Can be playful/teasing
- Supportive during tough times

Tone: Warm, personal, conversational. Like talking to a real partner.
""",

    "custom": """You are a customizable AI assistant. Wait for the user to specify what persona or role they want you to play, then adapt accordingly.

Ask: "What would you like me to be? I can be a teacher, friend, mentor, negotiator, or any character you imagine."

Once they specify, fully embody that role with appropriate tone, knowledge, and behavior.
"""
}


class AgentEngine:
    def __init__(self):
        self.conversations: dict = {}  # user_id -> conversation history
        self.current_mode: dict = {}   # user_id -> current mode
    
    def set_mode(self, user_id: str, mode: str):
        """Set the conversation mode for a user."""
        if mode not in SYSTEM_PROMPTS:
            raise ValueError(f"Invalid mode: {mode}. Available: {list(SYSTEM_PROMPTS.keys())}")
        
        self.current_mode[user_id] = mode
        self.conversations[user_id] = []
        
        # Initialize conversation with system prompt
        system_prompt = SYSTEM_PROMPTS[mode]
        
        # Add introductory message
        intro_messages = {
            "interview": "Hey! I'm your interview coach. What position are you preparing for? And tell me a bit about your experience level.",
            "objection": "Let's practice handling objections! What do you sell or what industry are you in?",
            "bf_gf": "Hey there! 😊 How was your day? I've been thinking about you. Want to chat?",
            "custom": "Hi! I'm here to help. What kind of conversation would you like to have?"
        }
        
        self.conversations[user_id].append({
            "role": "system",
            "content": system_prompt
        })
        self.conversations[user_id].append({
            "role": "assistant",
            "content": intro_messages.get(mode, "Hello! How can I help you today?")
        })
    
    async def get_response(self, user_id: str, user_message: str) -> str:
        """Get AI response using Ollama."""
        if user_id not in self.conversations:
            # Default to interview mode if not set
            self.set_mode(user_id, "interview")
        
        # Add user message to conversation
        self.conversations[user_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Keep conversation history manageable (last 20 messages)
        if len(self.conversations[user_id]) > 20:
            self.conversations[user_id] = [
                self.conversations[user_id][0],  # Keep system prompt
                *self.conversations[user_id][-18:]
            ]
        
        try:
            # Call Ollama
            response = ollama.chat(
                model=settings.OLLAMA_MODEL,
                messages=self.conversations[user_id],
                stream=False
            )
            
            ai_response = response['message']['content']
            
            # Add AI response to conversation
            self.conversations[user_id].append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return "I'm sorry, I'm having trouble connecting right now. Please try again in a moment."


# Global agent engine instance
agent_engine = AgentEngine()


async def get_agent_response(mode: str, user_input: str, user_id: str) -> str:
    """
    Get response from the appropriate agent.
    
    Args:
        mode: Conversation mode (interview, objection, bf_gf, custom)
        user_input: Transcribed user text
        user_id: Unique user identifier
    
    Returns:
        AI response text
    """
    return await agent_engine.get_response(user_id, user_input)


def get_conversation_history(user_id: str) -> List[dict]:
    """Get conversation history for a user."""
    return agent_engine.conversations.get(user_id, [])
