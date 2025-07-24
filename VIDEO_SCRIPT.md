# Video Script Outline (5 minutes)

## 1. Application Demo (1 minute)

### Opening (10 seconds)
"Welcome to the Agentic RAG Chatbot demonstration. This is a multi-agent system that can answer questions about your documents using advanced AI."

### Document Upload Demo (25 seconds)
1. Show the Streamlit interface
2. Upload sample documents (PDF, PPTX, CSV)
3. Click "Process Documents"
4. Show processing status and completion

### Question Answering Demo (25 seconds)
1. Ask: "What are the main KPIs mentioned in the documents?"
2. Show real-time processing
3. Display response with source attribution
4. Ask follow-up question: "Can you explain the performance metrics?"
5. Show multi-turn conversation capability

## 2. Architecture & Flow Explanation (2 minutes)

### System Overview (30 seconds)
"The system uses a 3-agent architecture with Model Context Protocol for communication:
- IngestionAgent: Processes and chunks documents
- RetrievalAgent: Performs semantic search using FAISS
- LLMResponseAgent: Generates responses using OpenAI GPT"

### MCP Communication (45 seconds)
"Agents communicate using structured messages with trace IDs for correlation. 
Let me show you the message flow..."

[Screen: Show MCP message structure diagram]

"When you upload a document:
1. UI sends INGESTION_REQUEST to IngestionAgent
2. IngestionAgent processes and sends INGESTION_COMPLETE to RetrievalAgent  
3. RetrievalAgent indexes the content for search"

### Query Processing Flow (45 seconds)
"When you ask a question:
1. UI sends RETRIEVAL_REQUEST to RetrievalAgent
2. RetrievalAgent finds relevant chunks and sends RETRIEVAL_RESULT to LLMResponseAgent
3. LLMResponseAgent combines context with your query and generates the final response"

[Screen: Show system flow diagram]

## 3. Code Explanation (2 minutes)

### Project Structure (30 seconds)
"Let's look at the code structure:
- app.py: Main Streamlit interface
- mcp/protocol.py: Message passing infrastructure  
- agents/: Three specialized agents
- utils/: Document processing utilities"

### MCP Implementation (45 seconds)
[Screen: Show mcp/protocol.py]
"The MCP protocol uses structured messages with sender, receiver, type, and payload.
The message bus handles routing and ensures reliable communication between agents."

### Agent Implementation (45 seconds)
[Screen: Show agents/retrieval_agent.py]
"Each agent subscribes to specific message types and implements async message handling.
The RetrievalAgent uses FAISS for vector similarity search with SentenceTransformers embeddings."

## Conclusion (30 seconds)
"This agentic architecture provides:
- Modular, scalable design
- Reliable inter-agent communication
- Support for multiple document formats
- Semantic search with source attribution

The complete code and documentation are available in the GitHub repository."

---

