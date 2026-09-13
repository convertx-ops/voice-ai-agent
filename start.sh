#!/bin/bash

echo "🚀 Starting Voice AI Agent..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Start the API server
echo "Starting FastAPI server on http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
echo ""

python main.py
