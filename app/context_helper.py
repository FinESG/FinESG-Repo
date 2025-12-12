"""
Token-based Context Manager
Implements 1200 token sliding window for conversation context
"""
from typing import List, Tuple
from sqlalchemy.orm import Session
from app import models

class TokenContextManager:
    def __init__(self, tokenizer, max_context_tokens: int = 1200):
        """
        Initialize context manager with token limit
        
        Args:
            tokenizer: HuggingFace tokenizer instance
            max_context_tokens: Maximum tokens for context window (default: 1200)
        """
        self.tokenizer = tokenizer
        self.max_context_tokens = max_context_tokens
    
    def build_context_from_messages(
        self,
        messages: List[models.Message],
        current_query: str = ""
    ) -> Tuple[str, dict]:
        """
        Build conversation context that fits within token limit
        
        Args:
            messages: List of Message objects from database (chronological order)
            current_query: The new user message
        
        Returns:
            Tuple of (context_string, metadata_dict)
        """
        # Start with current query
        current_tokens = len(self.tokenizer.encode(current_query))
        remaining_tokens = self.max_context_tokens - current_tokens
        
        # Build context from most recent messages backwards
        context_messages = []
        total_context_tokens = 0
        messages_included = 0
        was_truncated = False
        
        # Go backwards through messages
        for message in reversed(messages):
            message_text = f"{message.role.capitalize()}: {message.content}\n"
            message_tokens = len(self.tokenizer.encode(message_text))
            
            if total_context_tokens + message_tokens <= remaining_tokens:
                context_messages.insert(0, message_text)  # Insert at beginning to maintain order
                total_context_tokens += message_tokens
                messages_included += 1
            else:
                was_truncated = True
                break
        
        # Build final context string
        context_string = ""
        if context_messages:
            context_string = "Previous conversation:\n" + "".join(context_messages) + "\n"
        
        metadata = {
            "messages_included": messages_included,
            "context_tokens": total_context_tokens,
            "current_query_tokens": current_tokens,
            "total_tokens": total_context_tokens + current_tokens,
            "was_truncated": was_truncated,
            "max_tokens": self.max_context_tokens
        }
        
        return context_string, metadata
    
    def get_conversation_context(
        self,
        db: Session,
        conversation_id: int,
        current_query: str = ""
    ) -> Tuple[str, dict]:
        """
        Get conversation context from database
        
        Args:
            db: Database session
            conversation_id: ID of the conversation
            current_query: The new user message
        
        Returns:
            Tuple of (context_string, metadata_dict)
        """
        from app.crud import get_conversation_messages
        
        # Get all messages from conversation
        messages = get_conversation_messages(db, conversation_id)
        
        # Build context within token limit
        return self.build_context_from_messages(messages, current_query)
