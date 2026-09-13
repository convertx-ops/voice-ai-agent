#!/bin/bash

echo "🚀 Voice AI Agent - Setup Script"
echo "================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed"
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed"
    echo "   Download from: https://ollama.com/download"
    echo ""
    read -p "Press Enter to continue anyway (will use cloud API)..."
else
    echo "✅ Ollama found"
    
    # Check if model is pulled
    if ! ollama list | grep -q qwen2.5; then
        echo "📥 Pulling Qwen2.5 model..."
        ollama pull qwen2.5:3b
    else
        echo "✅ Qwen2.5 model ready"
    fi
fi

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env file and add your Telegram bot token!"
    echo "   Get a bot token from @BotFather on Telegram"
    echo ""
    read -p "Press Enter when ready to start..."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the API server:"
echo "  ./start.sh"
echo ""
echo "To start the Telegram bot:"
echo "  python bot.py"
echo ""
echo "To stop:"
echo "  Ctrl+C"
echo ""
