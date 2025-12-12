from app.database import SessionLocal
from app.models import User, Conversation, Message
from app.crud import *
from sqlalchemy import inspect

db = SessionLocal()

# Check tables
inspector = inspect(db.bind)
tables = inspector.get_table_names()
print(f"Tables: {tables}")

# Create user
user = User(email="test@example.com", hashed_password="test123")
db.add(user)
db.commit()
print(f"User created: {user.id}")

# Create conversation
conv = create_conversation(db, user.id, "Test Chat")
print(f"Conversation created: {conv.id}")

# Create messages
msg1 = create_message(db, conv.id, "user", "What is ESG?")
msg2 = create_message(db, conv.id, "assistant", "ESG stands for Environmental, Social, Governance")
print(f"Messages created: 2")

# Retrieve
messages = get_conversation_messages(db, conv.id)
print(f"Retrieved {len(messages)} messages")

db.close()
print("✓ All tests passed!")
