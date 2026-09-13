# Voice + Brain - Project Structure

```
voice-ai-agent/
│
├── main.py                 # Main entry point
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
│
├── voice/                  # Voice I/O
│   ├── __init__.py
│   ├── input.py           # Microphone recording + Whisper STT
│   └── output.py          # Piper/Edge TTS + audio playback
│
├── brain/                  # AI Brain
│   ├── __init__.py
│   └── llm.py             # Ollama integration + tool calling
│
├── memory/                 # Memory System
│   ├── __init__.py
│   └── memory.py          # Short + long-term memory
│
├── tools/                  # Tool Registry
│   ├── __init__.py
│   └── tools.py           # Calculator, file ops, etc.
│
├── data/                   # Runtime data
│   ├── memory/            # Saved memories (JSON)
│   ├── recordings/        # Audio recordings
│   └── audio/             # Generated speech
│
├── logs/                   # Application logs
│
└── docs/                   # Documentation
    └── ARCHITECTURE.md
```

## Module Responsibilities

### voice/input.py
- Microphone recording via sounddevice
- Audio format conversion (WAV)
- Speech transcription via Faster-Whisper
- Silence detection

### voice/output.py
- Text-to-speech generation
- Piper TTS (local/offline)
- Edge TTS (online fallback)
- Audio playback via sounddevice

### brain/llm.py
- Ollama client integration
- Conversation context management
- Tool calling orchestration
- Response generation

### memory/memory.py
- Short-term conversation memory
- Long-term persistent memory (JSON)
- Search and retrieval
- Memory statistics

### tools/tools.py
- Safe tool registry
- Calculator (safe eval)
- File operations (sandboxed)
- Memory save/retrieve

## Data Flow

```
User speaks → Microphone → WAV bytes → Whisper → Text
                                                                     ↓
                                                    LLM + Tools ← Context + Memory
                                                                     ↓
                                                  Response Text → TTS → Audio → Speakers
```

## Key Design Decisions

1. **Modular Architecture** - Each component is independently testable
2. **Offline-First** - All core functionality works without internet
3. **Safe Execution** - Tools are sandboxed with strict permissions
4. **Transparent Memory** - User controls what gets saved
5. **Graceful Degradation** - Falls back to online TTS if local fails