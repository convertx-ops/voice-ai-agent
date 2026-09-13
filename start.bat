@echo off
echo 🎙️  Voice + Brain System Setup
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.10+.
    pause
    exit /b 1
)

echo ✓ Python installed

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ================================================
echo ✓ Setup complete!
echo.
echo To start the assistant:
echo   start.bat
echo.
pause