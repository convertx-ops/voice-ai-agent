@echo off
echo ========================================
echo   Voice AI Agent - Deployment Guide
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

:: Create virtual environment
if not exist venv (
    echo [1/5] Creating virtual environment...
    python -m venv venv
)

:: Activate and install dependencies
echo [2/5] Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

:: Check Ollama
echo [3/5] Checking Ollama...
where ollama >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama not installed!
    echo Download from: https://ollama.com/download
    echo After installing, run: ollama pull qwen2.5:3b
) else (
    ollama list | findstr qwen2.5 >nul 2>&1
    if errorlevel 1 (
        echo Pulling Qwen2.5 model...
        ollama pull qwen2.5:3b
    )
)

:: Configure
echo [4/5] Configuring...
if not exist .env (
    copy .env.example .env
    echo [INFO] Created .env file - edit it and add your Telegram bot token!
)

echo [5/5] Starting server...
echo.
echo ========================================
echo   Server running at http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo To start Telegram bot in another window:
echo   python bot.py
echo.
pause
