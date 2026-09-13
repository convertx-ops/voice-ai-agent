#!/usr/bin/env python3
"""Test script for Voice + Brain System."""
import asyncio
import logging
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_config():
    """Test configuration loading."""
    from config import settings
    print(f"✓ Config loaded: {settings.APP_NAME} v{settings.VERSION}")
    print(f"  Model: {settings.OLLAMA_MODEL}")
    print(f"  TTS Engine: {settings.TTS_ENGINE}")
    return True


def test_imports():
    """Test all imports work."""
    try:
        from voice.input import VoiceInput
        from voice.output import VoiceOutput
        from brain.llm import LLMBrain
        from memory.memory import MemoryManager
        from tools.tools import ToolRegistry
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


async def test_llm():
    """Test LLM connection."""
    try:
        import ollama
        models = ollama.list()
        print(f"✓ Ollama connected")
        print(f"  Available models: {[m.get('name', 'unknown') for m in models.get('models', [])]}")
        return True
    except Exception as e:
        print(f"✗ Ollama error: {e}")
        return False


def test_memory():
    """Test memory system."""
    from memory.memory import memory_manager
    
    # Save test memory
    success = memory_manager.save_memory("test_key", "This is a test memory", "personal")
    if success:
        print("✓ Memory save works")
    else:
        print("✗ Memory save failed")
        return False
    
    # Retrieve test memory
    results = memory_manager.retrieve_memory("test")
    if results:
        print(f"✓ Memory retrieve works (found {len(results)} results)")
    else:
        print("✗ Memory retrieve failed")
        return False
    
    return True


def test_tools():
    """Test tool registry."""
    from tools.tools import tools
    
    # Test calculator
    result = tools.execute("calculator", {"expression": "2 + 2"})
    if result.get("result") == "4":
        print("✓ Calculator tool works")
    else:
        print(f"✗ Calculator failed: {result}")
        return False
    
    # Test time
    result = tools.execute("time", {})
    if "time" in result.get("result", "").lower():
        print("✓ Time tool works")
    else:
        print(f"✗ Time tool failed: {result}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Testing Voice + Brain System")
    print("="*60 + "\n")
    
    tests = [
        ("Configuration", test_config),
        ("Imports", test_imports),
        ("LLM Connection", test_llm),
        ("Memory System", test_memory),
        ("Tool Registry", test_tools),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n--- Testing: {name} ---")
        if asyncio.iscoroutinefunction(test_func):
            result = asyncio.run(test_func())
        else:
            result = test_func()
        results.append((name, result))
    
    print("\n" + "="*60)
    print("Test Results:")
    print("="*60)
    
    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {name}: {status}")
        if not result:
            all_passed = False
    
    print("="*60)
    if all_passed:
        print("\n✓ All tests passed! System is ready.")
        print("\nTo start the voice assistant:")
        print("  python main.py")
        return 0
    else:
        print("\n✗ Some tests failed. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())