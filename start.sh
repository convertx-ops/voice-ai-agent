#!/bin/bash
# Quick start script for Voice + Brain System

echo "🎙️  Voice + Brain System Setup"
echo "================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+."
    exit 1
fi

echo "✓ Python $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip not found."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check Ollama
echo ""
echo "Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not installed. Download from: https://ollama.com/download"
    echo "   After installation, run: ollama pull qwen2.5:3b"
else
    echo "✓ Ollama found"
    
    # Check if model is pulled
    if ! ollama list | grep -q "qwen2.5:3b"; then
        echo "Pulling model (this may take a few minutes)..."
        ollama pull qwen2.5:3b
    fi
fi

echo ""
echo "================================"
echo "✓ Setup complete!"
echo ""
echo "To start the assistant:"
echo "  ./start.sh"
echo ""
echo "Or run manually:"
echo "  source venv/bin/activate"
echo "  python main.py"