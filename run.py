#!/usr/bin/env python3
"""
Run script for the Agentic RAG Chatbot
"""

import os
import sys
import subprocess
import signal
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    try:
        import streamlit
        import openai
        import faiss
        import sentence_transformers
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check environment variables"""
    print("🔍 Checking environment...")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your_key_here'")
        return False
    
    print("✅ Environment variables are set")
    return True

def run_application():
    """Run the Streamlit application"""
    print("🚀 Starting Agentic RAG Chatbot...")
    
    try:
        # Run streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless=true",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false"
        ]
        
        process = subprocess.Popen(cmd)
        
        def signal_handler(sig, frame):
            print("\n🛑 Shutting down...")
            process.terminate()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        process.wait()
        
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("🤖 Agentic RAG Chatbot Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run from the project root directory.")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run application
    run_application()

if __name__ == "__main__":
    main()
