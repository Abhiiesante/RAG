from typing import List, Dict, Any, Optional
import asyncio
from mcp.protocol import MCPMessage, MCPMessageBus, MessageTypes
from utils.document_parsers import DocumentParser, DocumentChunker

class IngestionAgent:
    """Agent responsible for document ingestion and preprocessing"""
    
    def __init__(self, message_bus: MCPMessageBus):
        self.name = "IngestionAgent"
        self.message_bus = message_bus
        self.message_bus.subscribe(self.name, self.handle_message)
        self.processed_documents = {}
    
    async def handle_message(self, message: MCPMessage):
        """Handle incoming MCP messages"""
        if message.type == MessageTypes.INGESTION_REQUEST:
            await self.process_document(message)
    
    async def process_document(self, message: MCPMessage):
        """Process uploaded document and extract chunks"""
        try:
            payload = message.payload
            file_name = payload.get("file_name")
            file_content = payload.get("file_content")
            file_type = payload.get("file_type")
            
            print(f"📄 IngestionAgent: Processing {file_name} ({file_type})")
            
            # Parse document based on type
            chunks = await self._parse_document(file_content, file_type)
            
            # Further chunk large text pieces
            processed_chunks = []
            for chunk in chunks:
                content = chunk["content"]
                metadata = chunk["metadata"]
                
                # Apply chunking for large content
                if len(content) > 1000:
                    sub_chunks = DocumentChunker.chunk_text(content)
                    for i, sub_chunk in enumerate(sub_chunks):
                        processed_chunks.append({
                            "content": sub_chunk,
                            "metadata": {
                                **metadata,
                                "file_name": file_name,
                                "sub_chunk": i + 1
                            }
                        })
                else:
                    processed_chunks.append({
                        "content": content,
                        "metadata": {
                            **metadata,
                            "file_name": file_name
                        }
                    })
            
            # Store processed document
            self.processed_documents[file_name] = processed_chunks
            
            # Send completion message
            response_message = MCPMessage(
                sender=self.name,
                receiver="RetrievalAgent",
                msg_type=MessageTypes.INGESTION_COMPLETE,
                payload={
                    "file_name": file_name,
                    "chunks": processed_chunks,
                    "chunk_count": len(processed_chunks)
                },
                trace_id=message.trace_id
            )
            
            self.message_bus.publish(response_message)
            print(f"✅ IngestionAgent: Processed {len(processed_chunks)} chunks from {file_name}")
            
        except Exception as e:
            error_message = MCPMessage(
                sender=self.name,
                receiver=message.sender,
                msg_type=MessageTypes.ERROR,
                payload={
                    "error": str(e),
                    "stage": "document_processing"
                },
                trace_id=message.trace_id
            )
            self.message_bus.publish(error_message)
            print(f"❌ IngestionAgent Error: {str(e)}")
    
    async def _parse_document(self, file_content: bytes, file_type: str) -> List[Dict[str, Any]]:
        """Parse document based on its type"""
        file_type = file_type.lower()
        
        if file_type == "pdf":
            return DocumentParser.parse_pdf(file_content)
        elif file_type == "pptx":
            return DocumentParser.parse_pptx(file_content)
        elif file_type == "docx":
            return DocumentParser.parse_docx(file_content)
        elif file_type == "csv":
            return DocumentParser.parse_csv(file_content)
        elif file_type in ["txt", "md"]:
            return DocumentParser.parse_txt(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def get_processed_documents(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all processed documents"""
        return self.processed_documents
