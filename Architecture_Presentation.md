# Agentic RAG Chatbot Architecture Presentation

## Slide 1: Project Overview
**Agentic RAG Chatbot for Multi-Format Document QA using Model Context Protocol (MCP)**

### Key Features:
- 🤖 **Multi-Agent Architecture**: 3 specialized agents working together
- 📄 **Multi-Format Support**: PDF, PPTX, CSV, DOCX, TXT/Markdown
- 🔗 **MCP Integration**: Structured message passing between agents
- 🧠 **Semantic Search**: FAISS vector store with embeddings
- 💬 **Interactive UI**: Streamlit-based chat interface

---

## Slide 2: System Architecture

### Agent-Based Design with MCP:

```
┌─────────────────┐    MCP     ┌─────────────────┐    MCP     ┌─────────────────┐
│  IngestionAgent │◄──────────►│ RetrievalAgent  │◄──────────►│LLMResponseAgent │
│                 │            │                 │            │                 │
│ • Parse docs    │            │ • Generate      │            │ • Context       │
│ • Extract chunks│            │   embeddings    │            │   integration   │
│ • Preprocess   │            │ • FAISS search  │            │ • LLM response  │
└─────────────────┘            └─────────────────┘            └─────────────────┘
         │                              │                              │
         └──────────────────────────────┼──────────────────────────────┘
                                        │
                              ┌─────────▼─────────┐
                              │   MCP Message Bus │
                              │                   │
                              │ • Trace IDs       │
                              │ • Message routing │
                              │ • Error handling  │
                              └───────────────────┘
```

### MCP Message Structure:
```json
{
  "sender": "RetrievalAgent",
  "receiver": "LLMResponseAgent",
  "type": "RETRIEVAL_RESULT",
  "trace_id": "abc-123",
  "payload": {
    "retrieved_context": ["chunk1", "chunk2"],
    "query": "What are the KPIs?"
  }
}
```

---

## Slide 3: System Flow Diagram

### Document Processing & Query Flow:

```
1. 📤 USER UPLOADS DOCUMENTS
           │
           ▼
2. 📄 IngestionAgent
   • Parses PDF/PPTX/CSV/DOCX/TXT
   • Extracts & chunks content
   • Sends to RetrievalAgent
           │
           ▼
3. 🔍 RetrievalAgent  
   • Generates embeddings
   • Stores in FAISS index
   • Ready for queries
           │
           ▼
4. 💬 USER ASKS QUESTION
           │
           ▼
5. 🔍 RetrievalAgent
   • Semantic search
   • Returns top-k chunks
           │
           ▼
6. 🤖 LLMResponseAgent
   • Combines context + query
   • Calls OpenAI API
   • Returns final answer
           │
           ▼
7. 📱 UI DISPLAYS RESPONSE + SOURCES
```

---

## Slide 4: Tech Stack & Implementation

### Core Technologies:
- **Backend**: Python with asyncio
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-3.5/4
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **Document Processing**: PyMuPDF, python-pptx, python-docx, pandas

### Key Components:
- **MCP Protocol**: Custom message bus with structured communication
- **Agent Coordination**: Event-driven architecture with trace IDs
- **Document Parsers**: Format-specific extraction utilities
- **Chunking Strategy**: Overlapping chunks for better context

### File Structure:
```
RAG/
├── app.py                    # Main Streamlit app
├── agents/                   # Agent implementations
├── mcp/                      # Model Context Protocol
├── utils/                    # Document processing utilities
└── requirements.txt
```

---

## Slide 5: UI Screenshots & Demo

### Main Interface Features:
1. **Document Upload Panel**: 
   - Multi-file upload support
   - Format validation
   - Processing status

2. **Chat Interface**:
   - Multi-turn conversations
   - Source attribution
   - Relevance scores

3. **System Statistics**:
   - Total indexed chunks
   - Vector store metrics

### Demo Highlights:
- Upload multiple document formats
- Ask complex questions spanning multiple documents
- View source references with relevance scores
- Real-time processing with agent coordination

---

## Slide 6: Challenges & Future Scope

### Challenges Faced:
1. **Agent Coordination**: Implementing reliable MCP message passing
2. **Document Parsing**: Handling various formats consistently
3. **Chunking Strategy**: Balancing context size vs. retrieval precision
4. **Error Handling**: Graceful failure across agent pipeline
5. **UI Responsiveness**: Async processing in Streamlit

### Solutions Implemented:
- Trace IDs for message correlation
- Format-specific parsers with error handling
- Overlapping chunking with sentence boundaries
- Comprehensive error propagation via MCP
- Async/await patterns with progress indicators

### Future Improvements:
- **Enhanced Formats**: Excel, Images with OCR
- **Advanced Chunking**: Hierarchical or semantic chunking
- **Multi-Modal**: Image and table understanding
- **Agent Monitoring**: Performance metrics and logging
- **Distributed Deployment**: Microservices architecture
- **Real-time Collaboration**: Multi-user support

### Technical Enhancements:
- Graph-based retrieval for complex relationships
- Fine-tuned embeddings for domain-specific content
- Hybrid search combining keyword and semantic search
- Agent learning from user feedback

---

## Key Achievements:
✅ **Multi-Agent Architecture** with MCP communication
✅ **5 Document Formats** supported
✅ **Semantic Retrieval** with FAISS
✅ **Interactive UI** with source attribution
✅ **Scalable Design** for future enhancements
