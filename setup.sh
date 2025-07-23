#!/bin/bash

echo "🚀 Setting up Agentic RAG Chatbot..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Copy .env.example to .env and add your OpenAI API key"
echo "2. Run: source venv/bin/activate"
echo "3. Run: streamlit run app.py"
