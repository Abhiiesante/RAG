# Agentic RAG Chatbot - Complete Implementation Guide

## Project Overview

This project implements a sophisticated Retrieval-Augmented Generation (RAG) chatbot using an agentic architecture with Model Context Protocol (MCP) for inter-agent communication. The system can process multiple document formats and answer questions using semantic search and large language models.

## Architecture Components

### 1. Model Context Protocol (MCP)
- **File**: `mcp/protocol.py`
- **Purpose**: Structured message passing between agents
- **Features**:
  - Trace IDs for message correlation
  - Timestamp tracking
  - Type-safe message structure
  - In-memory message bus

### 2. Agents

#### IngestionAgent (`agents/ingestion_agent.py`)
- **Responsibility**: Document parsing and preprocessing
- **Supported Formats**: PDF, PPTX, CSV, DOCX, TXT/Markdown
- **Features**:
  - Format-specific parsers
  - Intelligent chunking
  - Metadata extraction

#### RetrievalAgent (`agents/retrieval_agent.py`)
- **Responsibility**: Embedding generation and semantic search
- **Technology**: FAISS vector store + SentenceTransformers
- **Features**:
  - Automatic embedding generation
  - Cosine similarity search
  - Relevance scoring

#### LLMResponseAgent (`agents/llm_response_agent.py`)
- **Responsibility**: Context integration and response generation
- **Technology**: OpenAI GPT models
- **Features**:
  - Context-aware prompting
  - Source attribution
  - Conversation history

#### CoordinatorAgent (`agents/coordinator_agent.py`)
- **Responsibility**: Workflow orchestration
- **Features**:
  - Session management
  - Flow coordination
  - Error handling

### 3. Document Processing (`utils/document_parsers.py`)
- **DocumentParser**: Format-specific parsing logic
- **DocumentChunker**: Intelligent text chunking with overlap
- **Features**:
  - Sentence boundary preservation
  - Metadata retention
  - Error handling

### 4. User Interface (`app.py`)
- **Technology**: Streamlit
- **Features**:
  - Multi-file upload
  - Real-time chat interface
  - Source attribution display
  - System statistics

## MCP Message Flow

### Document Upload Flow
```
UI → CoordinatorAgent → IngestionAgent → RetrievalAgent
```

### Query Processing Flow
```
UI → CoordinatorAgent → RetrievalAgent → LLMResponseAgent → UI
```

### Sample MCP Messages

#### Ingestion Request
```json
{
  "sender": "UI",
  "receiver": "IngestionAgent",
  "type": "INGESTION_REQUEST",
  "trace_id": "uuid-123",
  "payload": {
    "file_name": "document.pdf",
    "file_content": "binary_data",
    "file_type": "pdf"
  }
}
```

#### Retrieval Result
```json
{
  "sender": "RetrievalAgent",
  "receiver": "LLMResponseAgent",
  "type": "RETRIEVAL_RESULT",
  "trace_id": "uuid-123",
  "payload": {
    "query": "What are the KPIs?",
    "retrieved_context": ["context1", "context2"],
    "metadata": [{"file_name": "doc.pdf", "page": 1}]
  }
}
```

## Installation and Setup

### Prerequisites
- Python 3.9+
- OpenAI API key

### Local Setup
```bash
# Clone repository
git clone <repository-url>
cd RAG

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Run application
streamlit run app.py
```

### Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Usage Guide

### 1. Document Upload
1. Use the sidebar file uploader
2. Select multiple files (PDF, PPTX, CSV, DOCX, TXT)
3. Click "Process Documents"
4. Wait for processing completion

### 2. Asking Questions
1. Type questions in the chat interface
2. View responses with source attribution
3. Check relevance scores for retrieved context
4. Continue multi-turn conversations

### 3. System Monitoring
- Check sidebar for system statistics
- Monitor chunk count and index size
- View processing status in real-time

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: gpt-3.5-turbo)
- `EMBEDDING_MODEL`: Embedding model (default: all-MiniLM-L6-v2)
- `DEFAULT_TOP_K`: Number of chunks to retrieve (default: 5)
- `CHUNK_SIZE`: Text chunk size (default: 1000)
- `CHUNK_OVERLAP`: Chunk overlap (default: 200)

### Customization
Edit `config.py` to modify:
- Model parameters
- Chunk settings
- UI configuration
- File size limits

## Testing

Run the test suite:
```bash
python test_system.py
```

Tests include:
- MCP communication
- Document parsing
- Agent pipeline integration

## Performance Considerations

### Scalability
- In-memory vector store (FAISS) for fast retrieval
- Async processing for non-blocking operations
- Efficient chunking strategies

### Optimization Tips
- Use smaller embedding models for faster processing
- Adjust chunk size based on document types
- Configure appropriate top-k values for retrieval

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility

2. **OpenAI API Errors**
   - Verify API key is set correctly
   - Check API quota and rate limits

3. **Memory Issues**
   - Reduce chunk size or embedding dimensions
   - Process documents in smaller batches

4. **Processing Timeouts**
   - Increase timeout values in configuration
   - Check document file sizes

### Debug Mode
Set environment variable for verbose logging:
```bash
export DEBUG=1
streamlit run app.py
```

## Extending the System

### Adding New Document Formats
1. Add parser method to `DocumentParser` class
2. Update supported formats in configuration
3. Add format validation in UI

### Custom Agents
1. Create new agent class inheriting base structure
2. Implement `handle_message` method
3. Subscribe to relevant message types
4. Add to main application initialization

### Alternative Vector Stores
Replace FAISS implementation in `RetrievalAgent`:
- Chroma
- Pinecone
- Weaviate
- Qdrant

## Security Considerations

- API key management through environment variables
- Input validation for uploaded files
- File size limits to prevent DoS
- Sanitization of user queries

## Future Enhancements

### Planned Features
- Multi-modal document processing (images, tables)
- Advanced chunking strategies (semantic, hierarchical)
- Real-time collaboration features
- Performance monitoring dashboard
- Multi-language support

### Technical Improvements
- Distributed agent deployment
- Graph-based retrieval
- Fine-tuned domain embeddings
- Caching layer for frequently accessed content

## Contributing

1. Fork the repository
2. Create feature branch
3. Follow coding standards
4. Add tests for new features
5. Submit pull request

## License

This project is licensed under the MIT License.
