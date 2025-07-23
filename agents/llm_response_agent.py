from typing import List, Dict, Any, Optional
import asyncio
import os
from openai import OpenAI
from mcp.protocol import MCPMessage, MCPMessageBus, MessageTypes

class LLMResponseAgent:
    """Agent responsible for generating final responses using LLM"""
    
    def __init__(self, message_bus: MCPMessageBus, api_key: Optional[str] = None):
        self.name = "LLMResponseAgent"
        self.message_bus = message_bus
        self.message_bus.subscribe(self.name, self.handle_message)
        
        # Initialize OpenAI client
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
    
    async def handle_message(self, message: MCPMessage):
        """Handle incoming MCP messages"""
        if message.type == MessageTypes.RETRIEVAL_RESULT:
            await self.generate_response(message)
    
    async def generate_response(self, message: MCPMessage):
        """Generate response using retrieved context and LLM"""
        try:
            payload = message.payload
            query = payload.get("query")
            retrieved_context = payload.get("retrieved_context", [])
            metadata = payload.get("metadata", [])
            
            print(f"🤖 LLMResponseAgent: Generating response for: '{query}'")
            
            if not retrieved_context:
                # No context available
                response_message = MCPMessage(
                    sender=self.name,
                    receiver="UI",
                    msg_type=MessageTypes.LLM_RESPONSE,
                    payload={
                        "query": query,
                        "response": "I don't have any relevant information to answer your question. Please upload some documents first.",
                        "sources": [],
                        "context_used": False
                    },
                    trace_id=message.trace_id
                )
                self.message_bus.publish(response_message)
                return
            
            # Prepare context for LLM
            context_text = "\n\n".join([
                f"Source {i+1}: {context}" 
                for i, context in enumerate(retrieved_context)
            ])
            
            # Create prompt
            system_prompt = """You are a helpful AI assistant that answers questions based on provided context. 
            Use only the information from the given context to answer questions. 
            If the context doesn't contain enough information to answer the question, say so clearly.
            Always cite which sources you used in your answer."""
            
            user_prompt = f"""Context:
{context_text}

Question: {query}

Please provide a comprehensive answer based on the context above. If you reference information, mention which source number it came from."""
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            llm_response = response.choices[0].message.content
            
            # Prepare source information
            sources = []
            for i, meta in enumerate(metadata):
                source_info = {
                    "source_number": i + 1,
                    "file_name": meta.get("file_name", "Unknown"),
                    "page": meta.get("page"),
                    "slide": meta.get("slide"),
                    "paragraph": meta.get("paragraph"),
                    "similarity_score": meta.get("similarity_score", 0.0)
                }
                sources.append(source_info)
            
            # Update conversation history
            self.conversation_history.append({
                "query": query,
                "response": llm_response,
                "sources": sources
            })
            
            # Send final response
            response_message = MCPMessage(
                sender=self.name,
                receiver="UI",
                msg_type=MessageTypes.LLM_RESPONSE,
                payload={
                    "query": query,
                    "response": llm_response,
                    "sources": sources,
                    "context_used": True,
                    "context_count": len(retrieved_context)
                },
                trace_id=message.trace_id
            )
            
            self.message_bus.publish(response_message)
            print(f"✅ LLMResponseAgent: Generated response using {len(retrieved_context)} context sources")
            
        except Exception as e:
            error_message = MCPMessage(
                sender=self.name,
                receiver="UI",
                msg_type=MessageTypes.ERROR,
                payload={
                    "error": str(e),
                    "stage": "llm_generation"
                },
                trace_id=message.trace_id
            )
            self.message_bus.publish(error_message)
            print(f"❌ LLMResponseAgent Error: {str(e)}")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
