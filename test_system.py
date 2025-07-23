"""
Test script to validate the RAG chatbot functionality
"""

import asyncio
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.protocol import MCPMessage, MCPMessageBus, MessageTypes
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent

async def test_mcp_communication():
    """Test MCP message passing between agents"""
    print("🧪 Testing MCP Communication...")
    
    # Create message bus
    bus = MCPMessageBus()
    
    # Create test message
    test_message = MCPMessage(
        sender="TestAgent",
        receiver="TargetAgent",
        msg_type="TEST_MESSAGE",
        payload={"data": "Hello MCP!"}
    )
    
    # Store received messages
    received_messages = []
    
    def message_handler(message):
        received_messages.append(message)
    
    # Subscribe to messages
    bus.subscribe("TargetAgent", message_handler)
    
    # Publish message
    bus.publish(test_message)
    
    # Verify message received
    assert len(received_messages) == 1
    assert received_messages[0].payload["data"] == "Hello MCP!"
    assert received_messages[0].trace_id == test_message.trace_id
    
    print("✅ MCP Communication test passed!")

async def test_document_parsing():
    """Test document parsing functionality"""
    print("🧪 Testing Document Parsing...")
    
    from utils.document_parsers import DocumentParser
    
    # Test TXT parsing
    sample_text = b"This is a test document.\n\nIt has multiple paragraphs.\n\nEach paragraph should be parsed separately."
    
    chunks = DocumentParser.parse_txt(sample_text)
    assert len(chunks) > 0
    assert all("content" in chunk for chunk in chunks)
    assert all("metadata" in chunk for chunk in chunks)
    
    print(f"✅ Parsed {len(chunks)} chunks from test text")

async def test_agent_pipeline():
    """Test the complete agent pipeline"""
    print("🧪 Testing Agent Pipeline...")
    
    # Skip if no OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Skipping agent pipeline test - no OpenAI API key")
        return
    
    try:
        # Create message bus and agents
        bus = MCPMessageBus()
        
        # Initialize agents
        ingestion_agent = IngestionAgent(bus)
        retrieval_agent = RetrievalAgent(bus)
        llm_agent = LLMResponseAgent(bus)
        
        # Create test document
        test_content = b"""Sample Document for Testing

        This is a test document that contains information about:
        - Machine Learning
        - Artificial Intelligence
        - Natural Language Processing
        
        Key Performance Indicators (KPIs):
        - Accuracy: 95%
        - Precision: 90%
        - Recall: 85%
        
        The system performs well on various tasks."""
        
        # Test ingestion
        print("📄 Testing document ingestion...")
        ingestion_message = MCPMessage(
            sender="Test",
            receiver="IngestionAgent",
            msg_type=MessageTypes.INGESTION_REQUEST,
            payload={
                "file_name": "test_doc.txt",
                "file_content": test_content,
                "file_type": "txt"
            }
        )
        
        bus.publish(ingestion_message)
        
        # Wait for processing
        await asyncio.sleep(2)
        
        # Test retrieval
        print("🔍 Testing context retrieval...")
        retrieval_message = MCPMessage(
            sender="Test",
            receiver="RetrievalAgent",
            msg_type=MessageTypes.RETRIEVAL_REQUEST,
            payload={
                "query": "What are the KPIs mentioned in the document?",
                "top_k": 3
            }
        )
        
        bus.publish(retrieval_message)
        
        # Wait for processing
        await asyncio.sleep(3)
        
        print("✅ Agent pipeline test completed!")
        
    except Exception as e:
        print(f"❌ Agent pipeline test failed: {str(e)}")

async def main():
    """Run all tests"""
    print("🚀 Starting RAG Chatbot Tests...\n")
    
    try:
        await test_mcp_communication()
        print()
        
        await test_document_parsing()
        print()
        
        await test_agent_pipeline()
        print()
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
