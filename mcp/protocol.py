from dataclasses import dataclass
from typing import Any, Dict, Optional
import uuid
from datetime import datetime

@dataclass
class MCPMessage:
    """Model Context Protocol Message Structure"""
    sender: str
    receiver: str
    type: str
    trace_id: str
    timestamp: str
    payload: Dict[str, Any]
    
    def __init__(self, sender: str, receiver: str, msg_type: str, payload: Dict[str, Any], trace_id: Optional[str] = None):
        self.sender = sender
        self.receiver = receiver
        self.type = msg_type
        self.trace_id = trace_id or str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()
        self.payload = payload
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
            "payload": self.payload
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPMessage':
        return cls(
            sender=data["sender"],
            receiver=data["receiver"],
            msg_type=data["type"],
            payload=data["payload"],
            trace_id=data.get("trace_id")
        )

class MCPMessageBus:
    """Simple in-memory message bus for MCP communication"""
    
    def __init__(self):
        self.messages = []
        self.subscribers = {}
    
    def publish(self, message: MCPMessage):
        """Publish a message to the bus"""
        self.messages.append(message)
        
        # Notify subscribers
        if message.receiver in self.subscribers:
            for callback in self.subscribers[message.receiver]:
                callback(message)
    
    def subscribe(self, agent_name: str, callback):
        """Subscribe an agent to receive messages"""
        if agent_name not in self.subscribers:
            self.subscribers[agent_name] = []
        self.subscribers[agent_name].append(callback)
    
    def get_messages_for_trace(self, trace_id: str):
        """Get all messages for a specific trace"""
        return [msg for msg in self.messages if msg.trace_id == trace_id]

# Message Types
class MessageTypes:
    DOCUMENT_UPLOAD = "DOCUMENT_UPLOAD"
    INGESTION_REQUEST = "INGESTION_REQUEST"
    INGESTION_COMPLETE = "INGESTION_COMPLETE"
    RETRIEVAL_REQUEST = "RETRIEVAL_REQUEST"
    RETRIEVAL_RESULT = "RETRIEVAL_RESULT"
    LLM_REQUEST = "LLM_REQUEST"
    LLM_RESPONSE = "LLM_RESPONSE"
    CONTEXT_RESPONSE = "CONTEXT_RESPONSE"
    ERROR = "ERROR"
