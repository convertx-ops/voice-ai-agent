"""Main Voice + Brain Application."""
import asyncio
import logging
import sys
from typing import Optional
from datetime import datetime
import colorama
from colorama import Fore, Style, init

from config import settings
from voice.input import VoiceInput
from voice.output import VoiceOutput
from brain.llm import LLMBrain, brain
from memory.memory import memory_manager
from tools.tools import tools

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceBrainSystem:
    """
    Main system orchestrating voice input → brain → voice output.
    
    Flow:
    1. Listen for microphone input
    2. Transcribe speech to text
    3. Process through LLM with context and tools
    4. Generate response text
    5. Convert to speech and play
    """
    
    def __init__(self):
        self.voice_input = VoiceInput()
        self.voice_output = VoiceOutput()
        self.brain = brain
        self.running = False
        
        # Set system prompt
        self._set_system_prompt()
    
    def _set_system_prompt(self):
        """Set the system prompt for the AI."""
        prompt = f"""You are Voice + Brain, a helpful AI assistant with voice capabilities.

YOUR CAPABILITIES:
- You can answer questions and have conversations
- You have access to tools for calculations, file operations, and memory
- You remember things the user explicitly asks you to save
- You speak naturally and helpfully

MEMORY:
- Short-term: Current conversation context (last 20 messages)
- Long-term: Explicitly saved memories using "remember" tool
- Use memory tools when appropriate

TOOL USAGE:
- Use calculator for math
- Use time for current date/time
- Use remember to save important information
- Use search_memory to retrieve saved info
- Use read_file/list_files for local file operations

BEHAVIOR:
- Be concise but helpful
- Ask clarifying questions when needed
- Admit when you don't know something
- Never pretend to have capabilities you don't have
- Always be honest about limitations

REMEMBER: This is a voice conversation. Keep responses natural and conversational, not overly long.
"""
        self.brain.set_system_prompt(prompt)
    
    async def process_voice(self, max_duration: int = 30) -> bool:
        """
        Process one complete voice interaction cycle.
        
        Returns True if successful, False otherwise.
        """
        print(f"\n{Fore.CYAN}🎤 Listening...{Style.RESET_ALL}")
        
        # Record and transcribe
        text, success = self.voice_input.record_and_transcribe(max_duration)
        
        if not success or not text:
            print(f"{Fore.YELLOW}⚠️ Could not understand. Try again.{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.GREEN}👤 You said: {text}{Style.RESET_ALL}")
        
        # Process through brain
        print(f"{Fore.MAGENTA}🧠 Thinking...{Style.RESET_ALL}")
        result = self.brain.get_response(text)
        
        # Handle tool calls
        if result.get("tools_called"):
            for tool_call in result["tools_called"]:
                tool_name = tool_call["tool"]
                output = tool_call["output"]
                print(f"{Fore.BLUE}🔧 Tool [{tool_name}]: {output[:100]}...{Style.RESET_ALL}")
                
                # Add tool result to context
                self.brain.add_message("tool", str(output))
        
        # Get final response text
        response_text = result.get("text", "")
        
        if not response_text:
            print(f"{Fore.YELLOW}⚠️ No response generated.{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.WHITE}🤖 Assistant: {response_text}{Style.RESET_ALL}")
        
        # Speak response
        if settings.ENABLE_TTS:
            print(f"{Fore.CYAN}🔊 Speaking...{Style.RESET_ALL}")
            self.voice_output.speak(response_text)
        
        # Save to conversation memory
        memory_manager.add_to_conversation("user", text)
        memory_manager.add_to_conversation("assistant", response_text)
        
        return True
    
    def run_interactive(self):
        """Run interactive voice conversation loop."""
        print("\n" + "="*60)
        print(f"{Fore.BOLD}🎙️  Voice + Brain System v{settings.VERSION}{Style.RESET_ALL}")
        print("="*60)
        print(f"\n{Fore.WHITE}Press ENTER to speak, type 'quit' to exit, 'clear' to reset conversation.{Style.RESET_ALL}\n")
        
        self.running = True
        
        try:
            while self.running:
                try:
                    user_input = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
                    
                    if not user_input:
                        # Voice mode - record from microphone
                        asyncio.run(self.process_voice())
                    elif user_input.lower() == 'quit':
                        print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                        break
                    elif user_input.lower() == 'clear':
                        self.brain.clear_context()
                        memory_manager.clear_conversation()
                        print(f"{Fore.CYAN}Conversation cleared.{Style.RESET_ALL}")
                    elif user_input.lower().startswith('remember '):
                        # Direct memory save command
                        key_value = user_input[9:].split(':', 1)
                        if len(key_value) == 2:
                            key, value = key_value
                            if memory_manager.save_memory(key.strip(), value.strip()):
                                print(f"{Fore.GREEN}✓ Memory saved: {key.strip()}{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.RED}✗ Failed to save memory{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}Usage: remember key:value{Style.RESET_ALL}")
                    elif user_input.lower().startswith('search '):
                        # Direct memory search
                        query = user_input[7:]
                        results = memory_manager.retrieve_memory(query)
                        if results:
                            print(f"{Fore.CYAN}Found memories:{Style.RESET_ALL}")
                            for r in results[:5]:
                                print(f"  • {r['key']}: {r['value'][:80]}...")
                        else:
                            print(f"{Fore.YELLOW}No memories found.{Style.RESET_ALL}")
                    elif user_input.lower() == 'memory':
                        # Show memory stats
                        stats = memory_manager.get_stats()
                        print(f"\n{Fore.CYAN}Memory Stats:{Style.RESET_ALL}")
                        print(f"  Conversation messages: {stats['conversation_messages']}")
                        print(f"  Long-term memories: {stats['long_term_memories']['total_memories']}")
                        print()
                    else:
                        # Text mode - send directly to brain
                        result = self.brain.get_response(user_input)
                        print(f"\n{Fore.WHITE}{result.get('text', '')}{Style.RESET_ALL}\n")
                        
                        # Also speak if TTS enabled
                        if settings.ENABLE_TTS and result.get('text'):
                            self.voice_output.speak(result['text'])
                        
                        memory_manager.add_to_conversation("user", user_input)
                        memory_manager.add_to_conversation("assistant", result.get('text', ''))
                
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Interrupted. Goodbye!{Style.RESET_ALL}")
                    break
                except EOFError:
                    break
                
        finally:
            self.running = False
    
    def stop(self):
        """Stop the system."""
        self.running = False


def main():
    """Entry point."""
    print(f"\n{Fore.BOLD}Starting Voice + Brain System...{Style.RESET_ALL}")
    
    # Check Ollama is running
    try:
        import ollama
        ollama.list()
        print(f"{Fore.GREEN}✓ Ollama is running{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}✗ Ollama is not running. Please start Ollama first.{Style.RESET_ALL}")
        print(f"  Error: {e}")
        sys.exit(1)
    
    # Check Whisper model
    try:
        from faster_whisper import WhisperModel
        logger.info("Testing Whisper model loading...")
    except ImportError:
        print(f"{Fore.RED}✗ faster-whisper not installed.{Style.RESET_ALL}")
        sys.exit(1)
    
    # Create and run system
    system = VoiceBrainSystem()
    
    try:
        system.run_interactive()
    except Exception as e:
        logger.error(f"System error: {e}", exc_info=True)
        print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()