#!/bin/bash

# BugFixer Bot Setup Script

echo "🤖 BugFixer Bot - Setup Script"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Setup environment file
if [ ! -f ".env" ]; then
    echo "Setting up environment file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your tokens:"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - GITHUB_TOKEN"
    echo "   - ANTHROPIC_API_KEY"
    echo ""
    echo "After editing .env, run: python bugfixer_bot.py"
else
    echo "✓ .env file already exists"
    echo ""
    echo "Ready to run! Execute: python bugfixer_bot.py"
fi

echo ""
echo "================================"
echo "Setup complete! 🎉"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API tokens"
echo "2. Run: python bugfixer_bot.py"
echo "3. Open Telegram and start chatting with your bot!"
