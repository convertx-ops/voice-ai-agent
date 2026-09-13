"""Memory System - Short-term and Long-term Memory."""
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from config import settings

logger = logging.getLogger(__name__)


class MemoryStore:
    """
    Persistent memory storage using JSON files.
    
    Supports:
    - Short-term memory (conversation context)
    - Long-term memory (explicitly saved facts)
    - Search and retrieval
    """
    
    def __init__(self):
        self.memory_dir = Path(settings.MEMORY_DIR)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory short-term cache
        self.short_term: Dict[str, Any] = {}
        self.long_term_file = self.memory_dir / "long_term.json"
        self.long_term: Dict[str, Any] = self._load_long_term()
    
    def _load_long_term(self) -> Dict[str, Any]:
        """Load long-term memory from disk."""
        if self.long_term_file.exists():
            try:
                with open(self.long_term_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load memory: {e}")
                return {}
        return {}
    
    def _save_long_term(self):
        """Save long-term memory to disk."""
        try:
            with open(self.long_term_file, 'w') as f:
                json.dump(self.long_term, f, indent=2)
            logger.debug("Long-term memory saved")
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
    
    def save(self, key: str, value: str, category: str = "personal") -> bool:
        """
        Save a memory item.
        
        Args:
            key: Unique identifier
            value: Memory content
            category: Category (personal, facts, preferences, events)
        
        Returns:
            True if saved successfully
        """
        try:
            entry = {
                "key": key,
                "value": value,
                "category": category,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Store in long-term memory
            self.long_term[key] = entry
            
            # Also add to short-term cache
            self.short_term[key] = entry
            
            # Persist to disk
            self._save_long_term()
            
            logger.info(f"Memory saved: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
            return False
    
    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve memories matching a query.
        
        Simple keyword matching (can be enhanced with embeddings later).
        """
        results = []
        query_lower = query.lower()
        
        for key, entry in self.long_term.items():
            # Check if query matches key or value
            if query_lower in key.lower() or query_lower in entry['value'].lower():
                results.append(entry)
        
        # Also check short-term cache
        for key, entry in self.short_term.items():
            if query_lower in key.lower() or query_lower in entry['value'].lower():
                if entry not in results:
                    results.append(entry)
        
        return results[:10]  # Return top 10 matches
    
    def get_all(self) -> Dict[str, Any]:
        """Get all memories."""
        return self.long_term
    
    def delete(self, key: str) -> bool:
        """Delete a memory."""
        if key in self.long_term:
            del self.long_term[key]
            if key in self.short_term:
                del self.short_term[key]
            self._save_long_term()
            logger.info(f"Memory deleted: {key}")
            return True
        return False
    
    def clear_short_term(self):
        """Clear short-term memory cache."""
        self.short_term.clear()
        logger.info("Short-term memory cleared")
    
    def stats(self) -> Dict[str, int]:
        """Get memory statistics."""
        return {
            "total_memories": len(self.long_term),
            "short_term_cached": len(self.short_term),
            "categories": self._count_categories()
        }
    
    def _count_categories(self) -> Dict[str, int]:
        """Count memories by category."""
        counts = {}
        for entry in self.long_term.values():
            cat = entry.get('category', 'unknown')
            counts[cat] = counts.get(cat, 0) + 1
        return counts


class ConversationMemory:
    """Manages short-term conversation memory."""
    
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []
        self.max_messages = 50
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation memory."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep within limit
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_history(self, last_n: int = 20) -> List[Dict[str, Any]]:
        """Get recent conversation history."""
        return self.messages[-last_n:]
    
    def clear(self):
        """Clear conversation memory."""
        self.messages.clear()
    
    def summary(self) -> str:
        """Get summary of conversation."""
        if not self.messages:
            return "No conversation yet"
        
        recent = self.messages[-5:] if len(self.messages) > 5 else self.messages
        return "\n".join([f"{m['role']}: {m['content'][:50]}..." for m in recent])


class MemoryManager:
    """
    Main memory manager coordinating short and long-term memory.
    """
    
    def __init__(self):
        self.short_term = ConversationMemory()
        self.long_term = MemoryStore()
    
    def save_memory(self, key: str, value: str, category: str = "personal") -> bool:
        """Save to long-term memory."""
        return self.long_term.save(key, value, category)
    
    def retrieve_memory(self, query: str) -> List[Dict]:
        """Retrieve from long-term memory."""
        return self.long_term.retrieve(query)
    
    def add_to_conversation(self, role: str, content: str):
        """Add to short-term conversation memory."""
        self.short_term.add_message(role, content)
    
    def get_conversation_history(self) -> List[Dict]:
        """Get recent conversation history."""
        return self.short_term.get_history()
    
    def clear_conversation(self):
        """Clear conversation memory."""
        self.short_term.clear()
    
    def get_stats(self) -> Dict:
        """Get memory statistics."""
        return {
            "conversation_messages": len(self.short_term.messages),
            "long_term_memories": self.long_term.stats()
        }
    
    def get_relevant_context(self, current_query: str) -> str:
        """Get relevant long-term memories for current query."""
        memories = self.long_term.retrieve(current_query)
        if memories:
            context = "\n".join([f"[{m['key']}]: {m['value']}" for m in memories[:5]])
            return f"\n\nRelevant memories:\n{context}"
        return ""


# Singleton instance
memory_manager = MemoryManager()