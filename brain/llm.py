"""LLM Brain - Ollama Integration with Context Management."""
import json
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import ollama

from config import settings

logger = logging.getLogger(__name__)


class LLMBrain:
    """
    LLM Brain using Ollama for local inference.
    
    Manages conversation context, tool calling, and responses.
    """
    
    # Tool definitions for function calling
    TOOL_DEFINITIONS = [
        {
            "type": "function",
            "function": {
                "name": "save_memory",
                "description": "Save information to long-term memory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string", "description": "Memory key/identifier"},
                        "value": {"type": "string", "description": "Memory content"},
                        "category": {"type": "string", "enum": ["personal", "facts", "preferences", "events"]}
                    },
                    "required": ["key", "value"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "retrieve_memory",
                "description": "Retrieve information from long-term memory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Perform mathematical calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "Mathematical expression"}
                    },
                    "required": ["expression"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_time",
                "description": "Get current date and time",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web for information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"]
                }
            }
        }
    ]
    
    def __init__(self):
        self.model = settings.OLLAMA_MODEL
        self.host = settings.OLLAMA_HOST
        self.context: List[Dict[str, Any]] = []
        self.max_context = settings.MAX_CONTEXT_MESSAGES
    
    def set_system_prompt(self, prompt: str):
        """Set the system prompt."""
        # Remove existing system message if present
        self.context = [m for m in self.context if m.get('role') != 'system']
        
        # Add new system prompt
        self.context.insert(0, {
            "role": "system",
            "content": prompt
        })
        logger.info("System prompt set")
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.context.append({
            "role": role,
            "content": content
        })
        
        # Keep context manageable
        if len(self.context) > self.max_context:
            # Keep system message and recent history
            self.context = [self.context[0]] + self.context[-(self.max_context-1):]
    
    def get_response(self, user_input: str) -> Dict[str, Any]:
        """
        Get response from LLM.
        
        Returns dict with:
        - text: Response text
        - tools_called: List of tools called
        - need_response: Whether we need to speak
        """
        # Add user message
        self.add_message("user", user_input)
        
        try:
            # Call Ollama with tool definitions
            response = ollama.chat(
                model=self.model,
                messages=self.context,
                tools=self.TOOL_DEFINITIONS,
                stream=False
            )
            
            ai_message = response['message']
            response_text = ai_message.get('content', '')
            tool_calls = ai_message.get('tool_calls', [])
            
            # Add AI response to context
            self.add_message("assistant", response_text)
            
            # Process tool calls
            tools_called = []
            for tool_call in tool_calls:
                func = tool_call['function']
                name = func['name']
                arguments = json.loads(func['arguments'])
                
                # Execute tool
                result = self._execute_tool(name, arguments)
                tools_called.append({
                    "tool": name,
                    "input": arguments,
                    "output": result
                })
                
                # Add tool result to context
                self.add_message("tool", json.dumps(result))
            
            return {
                "text": response_text,
                "tools_called": tools_called,
                "need_response": bool(response_text or tools_called)
            }
            
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return {
                "text": "I'm having trouble processing that right now.",
                "tools_called": [],
                "error": str(e),
                "need_response": True
            }
    
    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool call."""
        try:
            if tool_name == "calculator":
                return self._tool_calculator(arguments)
            elif tool_name == "get_time":
                return self._tool_get_time(arguments)
            elif tool_name == "web_search":
                return self._tool_web_search(arguments)
            elif tool_name == "save_memory":
                return self._tool_save_memory(arguments)
            elif tool_name == "retrieve_memory":
                return self._tool_retrieve_memory(arguments)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            logger.error(f"Tool execution error: {tool_name}: {e}")
            return {"error": str(e)}
    
    def _tool_calculator(self, args: Dict) -> str:
        """Execute calculator tool."""
        try:
            import math
            expression = args.get('expression', '')
            # Safe evaluation using only allowed functions
            allowed_names = {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "sqrt": math.sqrt, "len": len
            }
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return str(result)
        except Exception as e:
            return f"Error: {e}"
    
    def _tool_get_time(self, args: Dict) -> str:
        """Get current time tool."""
        now = datetime.now()
        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def _tool_web_search(self, args: Dict) -> str:
        """Web search tool (placeholder)."""
        query = args.get('query', '')
        # For now, return a placeholder
        return f"Search results for: {query}\n\n(Note: Web search requires additional setup)"
    
    def _tool_save_memory(self, args: Dict) -> str:
        """Save memory tool."""
        from memory import memory_manager
        key = args.get('key', '')
        value = args.get('value', '')
        category = args.get('category', 'personal')
        
        success = memory_manager.save(key, value, category)
        return f"Memory saved: {success}"
    
    def _tool_retrieve_memory(self, args: Dict) -> str:
        """Retrieve memory tool."""
        from memory import memory_manager
        query = args.get('query', '')
        results = memory_manager.retrieve(query)
        return json.dumps(results, indent=2)
    
    def clear_context(self):
        """Clear conversation context."""
        if self.context:
            # Keep system prompt
            system_prompt = next((m for m in self.context if m.get('role') == 'system'), None)
            self.context = [system_prompt] if system_prompt else []
            logger.info("Context cleared")
    
    def get_context_summary(self) -> Dict:
        """Get summary of current context."""
        return {
            "model": self.model,
            "message_count": len(self.context),
            "last_user_message": next(
                (m['content'] for m in reversed(self.context) if m.get('role') == 'user'),
                None
            )
        }


# Singleton instance
brain = LLMBrain()