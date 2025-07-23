# Agentic RAG Chatbot with Model Context Protocol (MCP)

An agent-based Retrieval-Augmented Generation (RAG) chatbot that can answer user questions using uploaded documents of various formats, implementing Model Context Protocol for inter-agent communication.

## Features

- **Multi-Format Document Support**: PDF, PPTX, CSV, DOCX, TXT/Markdown
- **Agentic Architecture**: 3 specialized agents with MCP communication
- **Vector Store**: FAISS-based semantic search with embeddings
- **Interactive UI**: Streamlit-based chat interface
- **Multi-turn Conversations**: Contextual question answering

## Architecture

### Agents
1. **IngestionAgent**: Parses and preprocesses documents
2. **RetrievalAgent**: Handles embedding and semantic retrieval
3. **LLMResponseAgent**: Forms final LLM query and generates answers

### Model Context Protocol (MCP)
Each agent communicates using structured MCP messages:
```json
{
  "sender": "RetrievalAgent",
  "receiver": "LLMResponseAgent", 
  "type": "CONTEXT_RESPONSE",
  "trace_id": "abc-123",
  "payload": {
    "top_chunks": ["...", "..."],
    "query": "What are the KPIs?"
  }
}
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RAG
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Upload Documents**: Use the file uploader to upload PDF, PPTX, CSV, DOCX, or TXT files
2. **Ask Questions**: Type your questions in the chat interface
3. **View Responses**: Get answers with source context and document references

## Tech Stack

- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-3.5/4
- **Embeddings**: OpenAI text-embedding-ada-002
- **Vector Store**: FAISS
- **Document Processing**: PyMuPDF, python-pptx, python-docx, pandas
- **Framework**: Python with asyncio for agent coordination

## System Flow

1. User uploads documents → IngestionAgent processes and chunks content
2. User asks question → RetrievalAgent finds relevant chunks using vector search
3. LLMResponseAgent combines context and generates final response
4. UI displays answer with source references

## Project Structure

```
RAG/
├── app.py                 # Main Streamlit application
├── agents/               # Agent implementations
│   ├── __init__.py
│   ├── ingestion_agent.py
│   ├── retrieval_agent.py
│   └── llm_response_agent.py
├── mcp/                  # Model Context Protocol
│   ├── __init__.py
│   └── protocol.py
├── utils/                # Utility functions
│   ├── __init__.py
│   └── document_parsers.py
├── requirements.txt
└── README.md
```

## Future Improvements

- Support for more document formats (Excel, Images with OCR)
- Advanced chunking strategies
- Multiple vector store backends
- Agent performance monitoring
- Real-time collaboration features