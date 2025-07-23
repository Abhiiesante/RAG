from typing import List, Dict, Any, Optional
import asyncio
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from mcp.protocol import MCPMessage, MCPMessageBus, MessageTypes

class RetrievalAgent:
    """Agent responsible for embedding generation and semantic retrieval"""
    
    def __init__(self, message_bus: MCPMessageBus, model_name: str = "all-MiniLM-L6-v2"):
        self.name = "RetrievalAgent"
        self.message_bus = message_bus
        self.message_bus.subscribe(self.name, self.handle_message)
        
        # Initialize embedding model
        print(f"🤖 RetrievalAgent: Loading embedding model {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
        self.chunks = []
        self.chunk_metadata = []
    
    async def handle_message(self, message: MCPMessage):
        """Handle incoming MCP messages"""
        if message.type == MessageTypes.INGESTION_COMPLETE:
            await self.index_chunks(message)
        elif message.type == MessageTypes.RETRIEVAL_REQUEST:
            await self.retrieve_context(message)
    
    async def index_chunks(self, message: MCPMessage):
        """Index document chunks for retrieval"""
        try:
            payload = message.payload
            file_name = payload.get("file_name")
            chunks = payload.get("chunks", [])
            
            print(f"🔍 RetrievalAgent: Indexing {len(chunks)} chunks from {file_name}")
            
            # Extract text content for embedding
            texts = [chunk["content"] for chunk in chunks]
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add to FAISS index
            self.index.add(embeddings)
            
            # Store chunks and metadata
            self.chunks.extend(texts)
            self.chunk_metadata.extend([chunk["metadata"] for chunk in chunks])
            
            print(f"✅ RetrievalAgent: Indexed {len(chunks)} chunks. Total chunks: {len(self.chunks)}")
            
        except Exception as e:
            error_message = MCPMessage(
                sender=self.name,
                receiver=message.sender,
                msg_type=MessageTypes.ERROR,
                payload={
                    "error": str(e),
                    "stage": "indexing"
                },
                trace_id=message.trace_id
            )
            self.message_bus.publish(error_message)
            print(f"❌ RetrievalAgent Error: {str(e)}")
    
    async def retrieve_context(self, message: MCPMessage):
        """Retrieve relevant context for a query"""
        try:
            payload = message.payload
            query = payload.get("query")
            top_k = payload.get("top_k", 5)
            
            print(f"🔍 RetrievalAgent: Retrieving context for: '{query}'")
            
            if len(self.chunks) == 0:
                # No documents indexed yet
                response_message = MCPMessage(
                    sender=self.name,
                    receiver="LLMResponseAgent",
                    msg_type=MessageTypes.RETRIEVAL_RESULT,
                    payload={
                        "query": query,
                        "retrieved_context": [],
                        "metadata": [],
                        "message": "No documents have been uploaded yet."
                    },
                    trace_id=message.trace_id
                )
                self.message_bus.publish(response_message)
                return
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)
            faiss.normalize_L2(query_embedding)
            
            # Search for similar chunks
            scores, indices = self.index.search(query_embedding, min(top_k, len(self.chunks)))
            
            # Prepare retrieved context
            retrieved_context = []
            metadata = []
            
            for score, idx in zip(scores[0], indices[0]):
                if idx != -1:  # Valid index
                    retrieved_context.append(self.chunks[idx])
                    metadata.append({
                        **self.chunk_metadata[idx],
                        "similarity_score": float(score)
                    })
            
            # Send retrieval results
            response_message = MCPMessage(
                sender=self.name,
                receiver="LLMResponseAgent",
                msg_type=MessageTypes.RETRIEVAL_RESULT,
                payload={
                    "query": query,
                    "retrieved_context": retrieved_context,
                    "metadata": metadata,
                    "top_k": len(retrieved_context)
                },
                trace_id=message.trace_id
            )
            
            self.message_bus.publish(response_message)
            print(f"✅ RetrievalAgent: Retrieved {len(retrieved_context)} relevant chunks")
            
        except Exception as e:
            error_message = MCPMessage(
                sender=self.name,
                receiver=message.sender,
                msg_type=MessageTypes.ERROR,
                payload={
                    "error": str(e),
                    "stage": "retrieval"
                },
                trace_id=message.trace_id
            )
            self.message_bus.publish(error_message)
            print(f"❌ RetrievalAgent Error: {str(e)}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get retrieval statistics"""
        return {
            "total_chunks": len(self.chunks),
            "index_size": self.index.ntotal,
            "embedding_dimension": self.embedding_dim
        }
