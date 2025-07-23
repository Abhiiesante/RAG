"""
Configuration settings for the RAG chatbot
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for RAG chatbot settings"""
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    
    # Embedding Settings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Retrieval Settings
    DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "5"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # UI Settings
    PAGE_TITLE = "Agentic RAG Chatbot"
    PAGE_ICON = "🤖"
    
    # File Upload Settings
    SUPPORTED_FORMATS = ['pdf', 'pptx', 'csv', 'docx', 'txt', 'md']
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    
    # Agent Settings
    MESSAGE_TIMEOUT = int(os.getenv("MESSAGE_TIMEOUT", "30"))
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_') and not callable(getattr(cls, key))
        }
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        
        return True
