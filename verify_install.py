#!/usr/bin/env python3
"""
Quick installation verification script
"""

def check_installation():
    """Verify all components are properly installed"""
    
    print("🔍 Verifying Agentic RAG Chatbot Installation")
    print("=" * 50)
    
    # Check Python version
    import sys
    print(f"✅ Python version: {sys.version}")
    
    # Check required imports
    try:
        import streamlit as st
        print(f"✅ Streamlit: {st.__version__}")
    except ImportError:
        print("❌ Streamlit not installed")
        return False
    
    try:
        import openai
        print(f"✅ OpenAI: {openai.__version__}")
    except ImportError:
        print("❌ OpenAI not installed")
        return False
    
    try:
        import faiss
        print("✅ FAISS: Available")
    except ImportError:
        print("❌ FAISS not installed")
        return False
    
    try:
        import sentence_transformers
        print(f"✅ SentenceTransformers: Available")
    except ImportError:
        print("❌ SentenceTransformers not installed")
        return False
    
    # Check project structure
    import os
    required_files = [
        "app.py",
        "mcp/protocol.py",
        "agents/ingestion_agent.py",
        "agents/retrieval_agent.py", 
        "agents/llm_response_agent.py",
        "utils/document_parsers.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            return False
    
    # Check environment
    import os
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OPENAI_API_KEY configured")
    else:
        print("⚠️  OPENAI_API_KEY not set (required for LLM functionality)")
    
    print("\n🎉 Installation verification complete!")
    print("\nTo run the application:")
    print("  python run.py")
    print("  or")
    print("  streamlit run app.py")
    
    return True

if __name__ == "__main__":
    check_installation()
