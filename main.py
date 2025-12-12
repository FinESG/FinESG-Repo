from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import router
from app import models, database, crud, auth, schemas
import os
import torch

# Create Database Tables
models.Base.metadata.create_all(bind=database.engine)

# Create default user on startup
def create_default_user():
    db = database.SessionLocal()
    try:
        # Check if default user exists
        default_email = "demo@example.com"
        user = crud.get_user_by_email(db, email=default_email)
        if not user:
            # Create default user
            user_data = schemas.UserCreate(email=default_email, password="demo123456")
            crud.create_user(db, user_data)
            print(f"Created default user: {default_email}")
        else:
            print(f"Default user already exists: {default_email}")
    finally:
        db.close()

create_default_user()

# Display GPU/CPU Status on Startup
print("\n" + "="*50)
if torch.cuda.is_available():
    print(f"🚀 GPU DETECTED: {torch.cuda.get_device_name(0)}")
    print(f"CUDA Version: {torch.version.cuda}")
else:
    print("⚠️  Running on CPU - No GPU detected")
print("="*50 + "\n")

app = FastAPI(title="AI Project Backend")

# Configure CORS - BOTH localhost and 127.0.0.1 for cookie auth
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:3000",
        "http://127.0.0.1:5173",  # Add 127.0.0.1 as well
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "public")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def read_root():
    """Serve the frontend index.html"""
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to the AI Project Backend. Go to /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
