import streamlit as st
import asyncio
import os
from typing import List, Dict, Any
import time
import uuid

# Import our agents and MCP
from mcp.protocol import MCPMessage, MCPMessageBus, MessageTypes
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent

class RAGChatbot:
    """Main RAG Chatbot Application"""
    
    def __init__(self):
        self.message_bus = MCPMessageBus()
        self.responses = {}
        self.setup_agents()
    
    def setup_agents(self):
        """Initialize all agents"""
        try:
            self.ingestion_agent = IngestionAgent(self.message_bus)
            self.retrieval_agent = RetrievalAgent(self.message_bus)
            
            # Check for OpenAI API key
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
                st.stop()
            
            self.llm_agent = LLMResponseAgent(self.message_bus, api_key)
            
            # Subscribe to UI responses
            self.message_bus.subscribe("UI", self.handle_ui_message)
            
        except Exception as e:
            st.error(f"Error initializing agents: {str(e)}")
            st.stop()
    
    def handle_ui_message(self, message: MCPMessage):
        """Handle messages sent to UI"""
        self.responses[message.trace_id] = message
    
    async def process_documents(self, uploaded_files):
        """Process uploaded documents through the agent pipeline"""
        if not uploaded_files:
            return
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, uploaded_file in enumerate(uploaded_files):
            file_name = uploaded_file.name
            file_content = uploaded_file.getvalue()
            file_type = uploaded_file.name.split('.')[-1]
            
            status_text.text(f"Processing {file_name}...")
            
            # Send ingestion request
            trace_id = str(uuid.uuid4())
            ingestion_message = MCPMessage(
                sender="UI",
                receiver="IngestionAgent",
                msg_type=MessageTypes.INGESTION_REQUEST,
                payload={
                    "file_name": file_name,
                    "file_content": file_content,
                    "file_type": file_type
                },
                trace_id=trace_id
            )
            
            self.message_bus.publish(ingestion_message)
            
            # Wait for processing to complete
            max_wait = 30  # 30 seconds timeout
            wait_time = 0
            while trace_id not in self.responses and wait_time < max_wait:
                await asyncio.sleep(0.1)
                wait_time += 0.1
            
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        status_text.text("✅ All documents processed!")
        progress_bar.empty()
        status_text.empty()
    
    async def ask_question(self, query: str) -> Dict[str, Any]:
        """Ask a question and get response from the agent pipeline"""
        trace_id = str(uuid.uuid4())
        
        # Send retrieval request
        retrieval_message = MCPMessage(
            sender="UI",
            receiver="RetrievalAgent", 
            msg_type=MessageTypes.RETRIEVAL_REQUEST,
            payload={
                "query": query,
                "top_k": 5
            },
            trace_id=trace_id
        )
        
        self.message_bus.publish(retrieval_message)
        
        # Wait for response
        max_wait = 30  # 30 seconds timeout
        wait_time = 0
        while trace_id not in self.responses and wait_time < max_wait:
            await asyncio.sleep(0.1)
            wait_time += 0.1
        
        if trace_id in self.responses:
            response_message = self.responses[trace_id]
            return response_message.payload
        else:
            return {
                "query": query,
                "response": "Sorry, I couldn't process your question. Please try again.",
                "sources": [],
                "context_used": False
            }

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Agentic RAG Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Agentic RAG Chatbot with MCP")
    st.markdown("**Upload documents and ask questions using our multi-agent RAG system**")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        with st.spinner("Initializing agents..."):
            st.session_state.chatbot = RAGChatbot()
    
    # Sidebar for document upload
    with st.sidebar:
        st.header("📁 Document Upload")
        
        uploaded_files = st.file_uploader(
            "Upload documents",
            type=['pdf', 'pptx', 'csv', 'docx', 'txt', 'md'],
            accept_multiple_files=True,
            help="Supported formats: PDF, PPTX, CSV, DOCX, TXT, Markdown"
        )
        
        if uploaded_files:
            st.write(f"📄 {len(uploaded_files)} file(s) uploaded")
            
            if st.button("🔄 Process Documents"):
                with st.spinner("Processing documents..."):
                    asyncio.run(st.session_state.chatbot.process_documents(uploaded_files))
                st.success("Documents processed successfully!")
        
        # Display system stats
        st.header("📊 System Stats")
        try:
            stats = st.session_state.chatbot.retrieval_agent.get_stats()
            st.metric("Total Chunks", stats['total_chunks'])
            st.metric("Index Size", stats['index_size'])
        except:
            st.info("No documents processed yet")
    
    # Main chat interface
    st.header("💬 Chat Interface")
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display sources if available
            if message["role"] == "assistant" and "sources" in message:
                if message["sources"]:
                    with st.expander("📚 Sources"):
                        for source in message["sources"]:
                            st.write(f"**Source {source['source_number']}:** {source['file_name']}")
                            if source.get('page'):
                                st.write(f"Page: {source['page']}")
                            if source.get('slide'):
                                st.write(f"Slide: {source['slide']}")
                            if source.get('similarity_score'):
                                st.write(f"Relevance: {source['similarity_score']:.3f}")
                            st.write("---")
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = asyncio.run(st.session_state.chatbot.ask_question(prompt))
            
            # Display response
            st.markdown(response_data.get("response", "Sorry, I couldn't generate a response."))
            
            # Display sources
            sources = response_data.get("sources", [])
            if sources:
                with st.expander("📚 Sources"):
                    for source in sources:
                        st.write(f"**Source {source['source_number']}:** {source['file_name']}")
                        if source.get('page'):
                            st.write(f"Page: {source['page']}")
                        if source.get('slide'):
                            st.write(f"Slide: {source['slide']}")
                        if source.get('similarity_score'):
                            st.write(f"Relevance: {source['similarity_score']:.3f}")
                        st.write("---")
            
            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_data.get("response", ""),
                "sources": sources
            })
    
    # Footer
    st.markdown("---")
    st.markdown("**Architecture:** IngestionAgent → RetrievalAgent → LLMResponseAgent with MCP communication")

if __name__ == "__main__":
    main()
