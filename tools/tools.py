"""Tools Module - Safe utility functions for the AI."""
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
import os
import subprocess
import re

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry of available tools with safety checks."""
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_builtins()
    
    def _register_builtins(self):
        """Register built-in safe tools."""
        self.register_tool("calculator", self._calc, {
            "description": "Calculate mathematical expressions",
            "parameters": {"type": "object", "properties": {
                "expression": {"type": "string"}
            }}
        })
        
        self.register_tool("time", self._get_time, {
            "description": "Get current date and time",
            "parameters": {"type": "object", "properties": {}}
        })
        
        self.register_tool("read_file", self._read_file, {
            "description": "Read contents of a text file",
            "parameters": {"type": "object", "properties": {
                "path": {"type": "string", "description": "File path (relative to home)"}
            }}
        })
        
        self.register_tool("list_files", self._list_files, {
            "description": "List files in a directory",
            "parameters": {"type": "object", "properties": {
                "path": {"type": "string", "description": "Directory path"}
            }}
        })
        
        self.register_tool("remember", self._remember, {
            "description": "Save information to memory",
            "parameters": {"type": "object", "properties": {
                "key": {"type": "string"},
                "value": {"type": "string"}
            }}
        })
        
        self.register_tool("search_memory", self._search_memory, {
            "description": "Search saved memories",
            "parameters": {"type": "object", "properties": {
                "query": {"type": "string"}
            }}
        })
    
    def register_tool(self, name: str, func, schema: Dict):
        """Register a tool."""
        self.tools[name] = {
            "name": name,
            "function": func,
            "schema": schema
        }
        logger.info(f"Registered tool: {name}")
    
    def execute(self, tool_name: str, arguments: Dict) -> Dict:
        """Execute a tool safely."""
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            result = self.tools[tool_name]["function"](**arguments)
            return {"result": result, "tool": tool_name}
        except Exception as e:
            logger.error(f"Tool execution error: {tool_name}: {e}")
            return {"error": str(e)}
    
    # Built-in tool implementations
    
    def _calc(self, expression: str) -> str:
        """Safe calculator."""
        try:
            # Only allow safe operations
            safe_chars = set("0123456789+-*/.() ")
            if not all(c in safe_chars for c in expression):
                return "Error: Invalid characters in expression"
            
            result = eval(expression, {"__builtins__": {}}, {})
            return str(result)
        except Exception as e:
            return f"Error: {e}"
    
    def _get_time(self) -> str:
        """Get current time."""
        now = datetime.now()
        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def _read_file(self, path: str) -> str:
        """Read a text file."""
        try:
            # Security: only allow reading from home directory
            home = os.path.expanduser("~")
            full_path = os.path.abspath(os.path.join(home, path))
            
            if not full_path.startswith(home):
                return "Error: Access denied - outside home directory"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Limit output size
                return content[:10000] if len(content) > 10000 else content
        except FileNotFoundError:
            return f"Error: File not found: {path}"
        except Exception as e:
            return f"Error: {e}"
    
    def _list_files(self, path: str = ".") -> str:
        """List files in directory."""
        try:
            home = os.path.expanduser("~")
            full_path = os.path.abspath(os.path.join(home, path))
            
            if not full_path.startswith(home):
                return "Error: Access denied - outside home directory"
            
            entries = os.listdir(full_path)
            return "\n".join(entries[:50])  # Limit to 50 entries
        except Exception as e:
            return f"Error: {e}"
    
    def _remember(self, key: str, value: str) -> str:
        """Remember something."""
        from memory.memory import memory_manager
        success = memory_manager.save_memory(key, value)
        return f"Saved: {key}" if success else "Failed to save"
    
    def _search_memory(self, query: str) -> str:
        """Search memories."""
        from memory.memory import memory_manager
        results = memory_manager.retrieve_memory(query)
        if results:
            return json.dumps(results, indent=2)[:2000]
        return "No memories found matching your query"


# Singleton instance
tools = ToolRegistry()