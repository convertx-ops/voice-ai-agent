#!/bin/bash

echo "🚀 Voice AI Agent - One-Click Deploy"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 not found${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Python $(python3 --version)${NC}"
}

check_pip() {
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}❌ pip3 not found${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ pip3 found${NC}"
}

check_ollama() {
    if ! command -v ollama &> /dev/null; then
        echo -e "${YELLOW}⚠️  Ollama not installed${NC}"
        echo "   Download: https://ollama.com/download"
        return 1
    fi
    
    # Check if model exists
    if ! ollama list | grep -q qwen2.5; then
        echo -e "${YELLOW}📥 Pulling Qwen2.5 model...${NC}"
        ollama pull qwen2.5:3b
    else
        echo -e "${GREEN}✅ Qwen2.5 model ready${NC}"
    fi
    return 0
}

setup_venv() {
    if [ ! -d "venv" ]; then
        echo -e "${GREEN}📦 Creating virtual environment...${NC}"
        python3 -m venv venv
    fi
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
}

install_deps() {
    echo -e "${GREEN}📥 Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
}

configure_bot() {
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠️  .env file not found${NC}"
        echo "   Creating from template..."
        cp .env.example .env
        echo ""
        echo -e "${YELLOW}📝 IMPORTANT: Edit .env and add your Telegram bot token!${NC}"
        echo "   Get token from @BotFather on Telegram"
        echo ""
        read -p "Press Enter when ready..."
    else
        echo -e "${GREEN}✅ Configuration found${NC}"
    fi
}

start_server() {
    echo ""
    echo -e "${GREEN}🚀 Starting Voice AI Agent...${NC}"
    echo ""
    echo "   API Server: http://localhost:8000"
    echo "   API Docs:   http://localhost:8000/docs"
    echo ""
    echo "   To start Telegram bot in another terminal:"
    echo "   $ python bot.py"
    echo ""
    echo "   Press Ctrl+C to stop"
    echo ""
    
    python main.py
}

# Main execution
echo ""
check_python
check_pip
check_ollama
setup_venv
install_deps
configure_bot
start_server
