from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ============================================
# USER SCHEMAS
# ============================================
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

# ============================================
# AUTH SCHEMAS
# ============================================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ============================================
# MESSAGE SCHEMAS
# ============================================
class MessageBase(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class MessageCreate(MessageBase):
    file_name: Optional[str] = None
    file_content: Optional[str] = None

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    file_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================
# CONVERSATION SCHEMAS
# ============================================
class ConversationBase(BaseModel):
    title: str = "New Chat"

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class ConversationWithMessages(ConversationResponse):
    """Conversation with full message history"""
    messages: List[MessageResponse] = []

# ============================================
# API REQUEST/RESPONSE SCHEMAS
# ============================================
class ChatRequest(BaseModel):
    """Request for sending a message"""
    message: str
    conversation_id: Optional[int] = None  # If None, creates new conversation

class ChatResponse(BaseModel):
    """Response after sending a message"""
    message: MessageResponse
    conversation_id: int
    conversation_title: str
