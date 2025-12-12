from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    conversations = relationship("Conversation", back_populates="owner", cascade="all, delete-orphan")

class Conversation(Base):
    """A conversation represents a chat session with multiple messages"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, default="New Chat")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")

class Message(Base):
    """Individual messages within a conversation"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)  # "user" or "assistant"
    content = Column(Text)
    file_name = Column(String, nullable=True)  # For file uploads
    file_content = Column(Text, nullable=True)  # Store full file content
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    conversation = relationship("Conversation", back_populates="messages")
