# 🎙️ Voice + Brain System

A free, open-source AI voice assistant with local processing.

**Architecture:** Microphone → Speech Recognition → LLM Brain → Text-to-Speech → Speakers

## Features

- 🎤 **Voice Input** - Real-time microphone recording with Whisper STT
- 🧠 **Local LLM** - Ollama-powered reasoning (Qwen2.5, DeepSeek, etc.)
- 🔊 **Voice Output** - Piper TTS (offline) or Edge TTS (online fallback)
- 💾 **Memory System** - Short-term context + long-term saved memories
- 🛠️ **Tools** - Calculator, file ops, memory management
- 💯 **100% Free** - All components run locally, no paid APIs required

## Requirements

### Hardware
- **CPU:** Modern multi-core processor (4+ cores recommended)
- **RAM:** 8GB minimum, 16GB recommended
- **Storage:** 10GB free for models
- **Microphone:** Any USB or built-in mic
- **Speakers:** Any audio output

### Software
- Python 3.10+
- Ollama (for LLM)
- ffmpeg (for audio processing)

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/convertx-ops/voice-ai-agent.git
cd voice-ai-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Ollama
Download from: https://ollama.com/download

### 4. Pull Model
```bash
# Recommended for performance
ollama pull qwen2.5:3b

# Alternatives (larger = smarter but slower)
ollama pull qwen2.5:7b
ollama pull deepseek-coder:6.7b
```

### 5. Install Piper TTS (Optional - for offline voice)
```bash
# Download voice model
wget https://github.com/rhasspy/piper/releases/download/models/en_US-lessac-medium.onnx
wget https://github.com/rhasspy/piper/releases/download/models/en_US-lessac-medium.onnx.json

# Place in ~/.local/share/piper/models/
mkdir -p ~/.local/share/piper/models
mv en_US-lessac-medium.onnx* ~/.local/share/piper/models/
```

### 6. Run
```bash
python main.py
```

## Usage

### Interactive Mode
```
Press ENTER to speak (voice mode)
Type text and press ENTER (text mode)
Type 'quit' to exit
Type 'clear' to reset conversation
Type 'memory' to see memory stats
```

### Commands
- `remember key:value` - Save to long-term memory
- `search query` - Search memories
- `clear` - Reset conversation

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────┐     ┌──────────┐     ┌──────────┐
│  MICROPHONE │────▶│   WHISPER    │────▶│  OLLAMA  │────▶│ PIPER/   │────▶│ SPEAKERS │
│   (Input)   │     │  (STT)       │     │  (Brain) │     │ EDGE     │     │  (Output)│
└─────────────┘     └──────────────┘     └─────────┘     │  (TTS)   │     └──────────┘
                                                         └──────────┘
                                                             ▲
                                                             │
                                              ┌──────────────┴──────────────┐
                                              │        TOOLS & MEMORY       │
                                              │  - Calculator               │
                                              │  - File Operations          │
                                              │  - Long-term Memory         │
                                              │  - Context Management       │
                                              └─────────────────────────────┘
```

## Configuration

Edit `.env` file (copy from `.env.example`):

```ini
# Ollama
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_HOST=http://localhost:11434

# Audio
SAMPLE_RATE=16000
CHUNK_SIZE=1024

# Whisper
WHISPER_MODEL=base      # base, small, medium
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8

# TTS
ENABLE_TTS=true
TTS_ENGINE=piper        # piper (offline) or edge (online)
PIPER_VOICE=en_US-lessac-medium
EDGE_VOICE=en-IN-PrabhatNeural

# Directories
MEMORY_DIR=./memory
RECORDINGS_DIR=./recordings
AUDIO_DIR=./audio
```

## Performance Characteristics

| Component | Latency | Notes |
|-----------|---------|-------|
| Whisper STT | 2-5 sec | Depends on audio length |
| Ollama LLM | 3-10 sec | Depends on model size |
| Piper TTS | 1-3 sec | Offline, fast |
| Edge TTS | 2-4 sec | Requires internet |
| **Total** | **6-22 sec** | End-to-end response |

## Limitations

1. **Local Processing Required** - All AI runs on your machine
2. **Hardware Dependent** - Speed depends on your CPU/RAM
3. **Model Size Trade-off** - Larger models = better quality but slower
4. **No Cloud Fallback** - Requires stable local setup
5. **Audio Quality** - Depends on microphone quality

## Security

- All processing happens locally
- No data sent to external servers (except optional Edge TTS)
- Safe file operations (restricted to home directory)
- No shell execution by default
- Memory is stored locally and encrypted at rest (optional)

## License

MIT License - Free for personal and commercial use.

## Support

- GitHub Issues: https://github.com/convertx-ops/voice-ai-agent/issues
- Documentation: See individual module files for details