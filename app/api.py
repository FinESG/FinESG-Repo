from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import timedelta

from app import models, schemas, crud, auth, database
from app.ml_engine_lmstudio import model_instance  # 200x faster with LM Studio!
from app.context_helper import TokenContextManager
from app.utils import extract_text_from_pdf

router = APIRouter()

# Cookie name for the token
COOKIE_NAME = "access_token"

# Initialize token context manager with 2048 token limit
if model_instance is not None:
    context_manager = TokenContextManager(
        tokenizer=model_instance.tokenizer,
        max_context_tokens=2048
    )
else:
    print("⚠️  WARNING: Model not loaded. Context manager disabled.")
    context_manager = None

# ============================================
# AUTH HELPERS
# ============================================
async def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please login first.",
        )
    return token

async def get_current_user_from_cookie(
    request: Request, 
    db: Session = Depends(database.get_db)
) -> models.User:
    token = await get_token_from_cookie(request)
    return await auth.get_current_user(token=token, db=db)

# ============================================
# AUTH ROUTES
# ============================================
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Register a new user"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.Token)
async def login(
    login_request: schemas.LoginRequest, 
    response: Response,
    db: Session = Depends(database.get_db)
):
    """Login and set auth cookie"""
    user = crud.get_user_by_email(db, email=login_request.email)
    if not user or not auth.verify_password(login_request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    
    # Set cookie
    response.set_cookie(
        key=COOKIE_NAME,
        value=access_token,
        httponly=True,
        max_age=1800,
        samesite="lax"
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response):
    """Logout and clear cookie"""
    response.delete_cookie(key=COOKIE_NAME)
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user(
    current_user: models.User = Depends(get_current_user_from_cookie)
):
    """Get current logged-in user"""
    return current_user

# ============================================
# CONVERSATION ROUTES
# ============================================
@router.get("/conversations", response_model=List[schemas.ConversationResponse])
async def get_conversations(
    request: Request,
    db: Session = Depends(database.get_db)
):
    """Get all conversations for the current user"""
    try:
        current_user = await get_current_user_from_cookie(request, db)
        user_id = current_user.id
    except:
        user_id = 1  # Demo user fallback
    
    conversations = crud.get_user_conversations(db, user_id)
    
    # Add message count to each conversation
    response_convs = []
    for conv in conversations:
        conv_data = schemas.ConversationResponse(
            id=conv.id,
            user_id=conv.user_id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=len(conv.messages)
        )
        response_convs.append(conv_data)
    
    return response_convs

@router.post("/conversations", response_model=schemas.ConversationResponse)
async def create_conversation(
    conversation: schemas.ConversationCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user_from_cookie)
):
    """Create a new conversation"""
    conv = crud.create_conversation(db, current_user.id, conversation.title)
    return schemas.ConversationResponse(
        id=conv.id,
        user_id=conv.user_id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        message_count=0
    )

@router.get("/conversations/{conversation_id}", response_model=schemas.ConversationWithMessages)
async def get_conversation(
    conversation_id: int,
    request: Request,
    db: Session = Depends(database.get_db)
):
    """Get a conversation with all its messages"""
    try:
        current_user = await get_current_user_from_cookie(request, db)
        user_id = current_user.id
    except:
        user_id = 1  # Demo user fallback
    
    conv = crud.get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get messages
    messages = crud.get_conversation_messages(db, conversation_id)
    
    return schemas.ConversationWithMessages(
        id=conv.id,
        user_id=conv.user_id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        message_count=len(messages),
        messages=[
            schemas.MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                file_name=msg.file_name,
                created_at=msg.created_at
            )
            for msg in messages
        ]
    )

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(database.get_db)
):
    """Delete a conversation"""
    # Flexible auth: try to get current user, fall back to demo user
    try:
        current_user = await get_current_user_from_cookie(Request, db)
        user_id = current_user.id
    except:
        user_id = 1  # Demo user fallback
    
    conv = crud.get_conversation(db, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    crud.delete_conversation(db, conversation_id)
    return {"message": "Conversation deleted"}

# ============================================
# MESSAGE / CHAT ROUTES
# ============================================
@router.post("/chat", response_model=schemas.ChatResponse)
async def send_message(
    request: Request,
    chat_request: schemas.ChatRequest,
    db: Session = Depends(database.get_db)
):
    """
    Send a message in a conversation
    
    This endpoint:
    1. Creates a new conversation if conversation_id is None
    2. Builds context from previous messages (1200 token limit)
    3. Calls model with context
    4. Saves user message and assistant response
    """
    try:
        current_user = await get_current_user_from_cookie(request, db)
        user_id = current_user.id
    except:
        user_id = 1  # Demo user fallback
    
    # Create new conversation if needed
    if chat_request.conversation_id is None:
        # Auto-generate title from first message
        title = chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message
        conv = crud.create_conversation(db, user_id, title)
        conversation_id = conv.id
    else:
        # Check if conversation exists
        conversation_id = chat_request.conversation_id
        conv = crud.get_conversation(db, conversation_id)
        if not conv:
            # Conversation doesn't exist - create it (frontend may send non-existent IDs)
            title = chat_request.message[:50] + "..." if len(chat_request.message) > 50 else chat_request.message
            conv = crud.create_conversation(db, user_id, title)
            conversation_id = conv.id
    
    # Verify model is loaded
    if model_instance is None:
        raise HTTPException(
            status_code=503,
            detail="AI model is not available. Please contact administrator."
        )
    
    if context_manager is None:
        raise HTTPException(
            status_code=503,
            detail="Context manager not initialized. Please contact administrator."
        )
    
    # Get conversation context (1200 tokens)
    context, metadata = context_manager.get_conversation_context(
        db, conversation_id, chat_request.message
    )
    
    print(f"📜 Context: {metadata['messages_included']} messages, "
          f"{metadata['context_tokens']} tokens, truncated={metadata['was_truncated']}")
    
    # Call model WITH CONTEXT
    assistant_response = model_instance.predict(chat_request.message, context)
    
    # Save user message
    user_msg = crud.create_message(
        db, conversation_id, "user", chat_request.message
    )
    
    # Save assistant response
    assistant_msg = crud.create_message(
        db, conversation_id, "assistant", assistant_response
    )
    
    # Get updated conversation
    conv = crud.get_conversation(db, conversation_id)
    
    return schemas.ChatResponse(
        message=schemas.MessageResponse(
            id=assistant_msg.id,
            conversation_id=assistant_msg.conversation_id,
            role=assistant_msg.role,
            content=assistant_msg.content,
            file_name=assistant_msg.file_name,
            created_at=assistant_msg.created_at
        ),
        conversation_id=conversation_id,
        conversation_title=conv.title
    )

@router.post("/chat/file", response_model=schemas.ChatResponse)
async def send_message_with_file(
    request: Request,
    file: UploadFile = File(...),
    conversation_id: Optional[int] = None,
    db: Session = Depends(database.get_db)
):
    """
    Upload a file and analyze it
    
    Accepts PDF or TXT files, extracts content, and processes with model
    """
    # Validate file type
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
    
    # Read file
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    
    # Extract text
    if file.content_type == "application/pdf":
        file_text = extract_text_from_pdf(content)
    else:
        file_text = content.decode("utf-8")
    
    if not file_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file")
    
    # Try to get current user, fallback to demo user
    try:
        current_user = await get_current_user_from_cookie(request, db)
        user_id = current_user.id
    except:
        user_id = 1
    
    # Create conversation if needed
    if conversation_id is None:
        conv = crud.create_conversation(db, user_id, f"File: {file.filename}")
        conversation_id = conv.id
    else:
        conv = crud.get_conversation(db, conversation_id)
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get context
    user_message = f"Analyze this file: {file.filename}"
    
    # Verify model is loaded
    if model_instance is None or context_manager is None:
        raise HTTPException(
            status_code=503,
            detail="AI model is not available. Please contact administrator."
        )
    
    context, metadata = context_manager.get_conversation_context(
        db, conversation_id, file_text
    )
    
    # Call model
    assistant_response = model_instance.predict(file_text, context)
    
    # Save user message with file
    user_msg = crud.create_message(
        db, conversation_id, "user", user_message,
        file_name=file.filename,
        file_content=file_text
    )
    
    # Save assistant response
    assistant_msg = crud.create_message(
        db, conversation_id, "assistant", assistant_response
    )
    
    conv = crud.get_conversation(db, conversation_id)
    
    return schemas.ChatResponse(
        message=schemas.MessageResponse(
            id=assistant_msg.id,
            conversation_id=assistant_msg.conversation_id,
            role=assistant_msg.role,
            content=assistant_msg.content,
            file_name=assistant_msg.file_name,
            created_at=assistant_msg.created_at
        ),
        conversation_id=conversation_id,
        conversation_title=conv.title
    )

# ============================================
# LEGACY COMPATIBILITY (for existing frontend)
# ============================================
@router.post("/predict")
async def predict_legacy(
    request: Request,
    db: Session = Depends(database.get_db)
):
    """
    DEPRECATED: Legacy endpoint - Use /chat instead
    This endpoint will be removed in a future version.
    Please migrate to the new /chat endpoint for text messages.
    """
    import warnings
    warnings.warn("The /predict endpoint is deprecated. Use /chat instead.", DeprecationWarning)
    
    data = await request.json()
    message = data.get("text", "")
    
    # Try to get current user
    try:
        current_user = await get_current_user_from_cookie(request, db)
        user_id = current_user.id
    except:
        # If no auth, use demo user (id=1)
        user_id = 1
    
    # Create or get conversation
    convs = crud.get_user_conversations(db, user_id, limit=1)
    if convs:
        conversation_id = convs[0].id
    else:
        conv = crud.create_conversation(db, user_id, "Chat")
        conversation_id = conv.id
    
    # Verify model is loaded
    if model_instance is None or context_manager is None:
        return {
            "id": conversation_id,
            "input_text": message,
            "output_text": "Error: AI model is currently unavailable. Please try again later."
        }
    
    # Get context and call model
    context, _ = context_manager.get_conversation_context(db, conversation_id, message)
    response = model_instance.predict(message, context)
    
    # Save messages
    crud.create_message(db, conversation_id, "user", message)
    crud.create_message(db, conversation_id, "assistant", response)
    
    return {"id": conversation_id, "input_text": message, "output_text": response}

@router.get("/history")
async def get_history_legacy(
    request: Request,
    db: Session = Depends(database.get_db)
):
    """
    DEPRECATED: Legacy endpoint - Use /conversations instead
    This endpoint will be removed in a future version.
    """
    import warnings
    warnings.warn("The /history endpoint is deprecated. Use /conversations instead.", DeprecationWarning)
    
    try:
        current_user = await get_current_user_from_cookie(request, db)
        user_id = current_user.id
    except:
        user_id = 1
    
    # Get conversations and convert to old format
    conversations = crud.get_user_conversations(db, user_id, limit=50)
    
    legacy_chats = []
    for conv in conversations:
        messages = crud.get_conversation_messages(db, conv.id, limit=2)
        if messages:
            # Combine first user/assistant pair as one "chat"
            user_msg = next((m for m in messages if m.role == "user"), None)
            asst_msg = next((m for m in messages if m.role == "assistant"), None)
            
            if user_msg and asst_msg:
                legacy_chats.append({
                    "id": conv.id,
                    "input_text": user_msg.content,
                    "output_text": asst_msg.content,
                    "timestamp": conv.created_at
                })
    
    return legacy_chats
