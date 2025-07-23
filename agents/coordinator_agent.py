from typing import Dict, Any, Optional
import asyncio
from mcp.protocol import MCPMessage, MCPMessageBus, MessageTypes

class CoordinatorAgent:
    """Coordinator agent that manages the overall RAG workflow"""
    
    def __init__(self, message_bus: MCPMessageBus):
        self.name = "CoordinatorAgent"
        self.message_bus = message_bus
        self.message_bus.subscribe(self.name, self.handle_message)
        self.active_sessions = {}
    
    async def handle_message(self, message: MCPMessage):
        """Handle incoming coordination requests"""
        if message.type == "USER_QUERY":
            await self.coordinate_query_flow(message)
        elif message.type == "DOCUMENT_UPLOAD":
            await self.coordinate_ingestion_flow(message)
    
    async def coordinate_query_flow(self, message: MCPMessage):
        """Coordinate the query processing flow across agents"""
        trace_id = message.trace_id
        query = message.payload.get("query")
        
        print(f"🎯 CoordinatorAgent: Coordinating query flow for '{query}'")
        
        # Step 1: Request retrieval
        retrieval_request = MCPMessage(
            sender=self.name,
            receiver="RetrievalAgent",
            msg_type=MessageTypes.RETRIEVAL_REQUEST,
            payload={
                "query": query,
                "top_k": 5
            },
            trace_id=trace_id
        )
        
        self.message_bus.publish(retrieval_request)
        
        # The retrieval agent will automatically forward to LLM agent
        # No further coordination needed due to the pipeline design
    
    async def coordinate_ingestion_flow(self, message: MCPMessage):
        """Coordinate document ingestion across agents"""
        trace_id = message.trace_id
        payload = message.payload
        
        print(f"🎯 CoordinatorAgent: Coordinating ingestion for {payload.get('file_name')}")
        
        # Forward to ingestion agent
        ingestion_request = MCPMessage(
            sender=self.name,
            receiver="IngestionAgent",
            msg_type=MessageTypes.INGESTION_REQUEST,
            payload=payload,
            trace_id=trace_id
        )
        
        self.message_bus.publish(ingestion_request)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about active sessions"""
        return {
            "active_sessions": len(self.active_sessions),
            "total_processed": len([s for s in self.active_sessions.values() if s.get("completed")])
        }
