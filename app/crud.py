from sqlalchemy.orm import Session
from sqlalchemy import desc
from app import models, schemas, auth
from typing import List, Optional

# ============================================
# USER CRUD
# ============================================
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ============================================
# CONVERSATION CRUD
# ============================================
def create_conversation(db: Session, user_id: int, title: str = "New Chat") -> models.Conversation:
    """Create a new conversation for a user"""
    conversation = models.Conversation(
        user_id=user_id,
        title=title
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_conversation(db: Session, conversation_id: int) -> Optional[models.Conversation]:
    """Get a conversation by ID"""
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def get_user_conversations(db: Session, user_id: int, limit: int = 50) -> List[models.Conversation]:
    """Get all conversations for a user"""
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.user_id == user_id)
        .order_by(desc(models.Conversation.updated_at))
        .limit(limit)
        .all()
    )

def delete_conversation(db: Session, conversation_id: int):
    """Delete a conversation and all its messages"""
    conversation = get_conversation(db, conversation_id)
    if conversation:
        db.delete(conversation)
        db.commit()
        return True
    return False

# ============================================
# MESSAGE CRUD
# ============================================
def create_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
    file_name: Optional[str] = None,
    file_content: Optional[str] = None
) -> models.Message:
    """Create a new message in a conversation"""
    message = models.Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        file_name=file_name,
        file_content=file_content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # Update conversation's updated_at timestamp
    conversation = get_conversation(db, conversation_id)
    if conversation:
        from datetime import datetime, timezone
        conversation.updated_at = datetime.now(timezone.utc)
        db.commit()
    
    return message

def get_conversation_messages(
    db: Session,
    conversation_id: int,
    limit: Optional[int] = None
) -> List[models.Message]:
    """Get all messages in a conversation"""
    query = (
        db.query(models.Message)
        .filter(models.Message.conversation_id == conversation_id)
        .order_by(models.Message.created_at)
    )
    
    if limit:
        query = query.limit(limit)
    
    return query.all()

def get_recent_messages(
    db: Session,
    conversation_id: int,
    limit: int = 10
) -> List[models.Message]:
    """Get most recent messages from a conversation"""
    return (
        db.query(models.Message)
        .filter(models.Message.conversation_id == conversation_id)
        .order_by(desc(models.Message.created_at))
        .limit(limit)
        .all()
    )[::-1]  # Reverse to chronological order
