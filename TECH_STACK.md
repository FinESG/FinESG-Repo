# Tech Stack - ESG Reporter Project

## 📋 Overview

ESG Reporter is a full-stack AI-powered application for analyzing ESG (Environmental, Social, Governance) reports and financial documents using a fine-tuned language model.

---

## 🎨 Frontend Stack

### Core Framework

- **React** 18+ - Component-based UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Next-generation frontend build tool

### UI & Styling

- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality component library
- **Lucide React** - Beautiful icon set

### State Management

- **React Context API**
  - `ChatContext` - Manages conversations and messages
  - `AuthContext` - Handles user authentication state

### HTTP Client

- **Fetch API** - Native browser HTTP client with credentials support

### Development Server

- **Vite Dev Server** - Fast HMR (Hot Module Replacement)
- Port: `5173`

---

## ⚙️ Backend Stack

### Core Framework

- **Python** 3.13
- **FastAPI** - Modern, fast async web framework
- **Uvicorn** - Lightning-fast ASGI server

### Database Layer

- **SQLAlchemy** - Python SQL toolkit and ORM
- **SQLite** - Embedded relational database
- Schema:
  - Users (authentication)
  - Conversations (chat sessions)
  - Messages (chat history)

### Authentication & Security

- **python-jose[cryptography]** - JWT token creation/verification
- **passlib[bcrypt]** - Secure password hashing
- **python-multipart** - File upload handling
- **HTTPOnly Cookies** - Secure token storage

### Data Validation

- **Pydantic** - Data validation using Python type annotations

### API Design

- **RESTful API** architecture
- **CORS** enabled for frontend communication
- Cookie-based authentication with flexible demo mode

---

## 🤖 AI/ML Stack

### Inference Engine

- **LM Studio** - Local model serving platform
  - Optimized GGUF inference
  - OpenAI-compatible API
  - Port: `1234`

### Model Architecture

- **Base Model**: Qwen 2.5-1.5B-Instruct
- **Fine-tuned Adapter**: fingesg4 (ESG-specialized)
- **Format**: GGUF (Q4_K_M quantization)
- **Performance**: 150+ tokens/second
- **Context Window**: 4096 tokens
- **Max Output**: 2000 tokens

### Integration

- **OpenAI Python Client** - Communicates with LM Studio API
- **Custom Tokenizer** - Simple token counting for context management

### Original ML Stack (Deprecated)

- ~~Transformers (Hugging Face)~~
- ~~PyTorch~~
- ~~PEFT (Parameter-Efficient Fine-Tuning)~~
- *Replaced by LM Studio for 200x faster inference*

---

## 🗄️ Data Flow Architecture

```
┌─────────────┐
│   Frontend  │ (React + Vite)
│  Port: 5173 │
└──────┬──────┘
       │ REST API (HTTP + Cookies)
       ▼
┌─────────────┐
│   Backend   │ (FastAPI + SQLAlchemy)
│  Port: 8080 │
└──────┬──────┘
       │
       ├─────► SQLite Database (Conversations, Messages)
       │
       └─────► LM Studio API (AI Inference)
               Port: 1234
               
```

---

## 📦 Key Dependencies

### Backend (`requirements.txt`)

```
fastapi
uvicorn[standard]
sqlalchemy
pydantic
python-jose[cryptography]
passlib[bcrypt]
python-multipart
openai
transformers
peft
accelerate
torch
```

### Frontend (`package.json`)

```json
{
  "dependencies": {
    "react": "^18.x",
    "react-dom": "^18.x",
    "lucide-react": "latest",
    "class-variance-authority": "latest",
    "clsx": "latest",
    "tailwind-merge": "latest"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "latest",
    "typescript": "latest",
    "tailwindcss": "latest",
    "autoprefixer": "latest",
    "postcss": "latest",
    "vite": "latest"
  }
}
```

---

## 🚀 Key Features

### ✅ Core Functionality

- **ESG Analysis** - AI-powered sustainability and governance reporting
- **PDF Upload** - Analyze annual reports and financial documents
- **Chat Interface** - Multi-turn conversations with context awareness
- **Conversation History** - Persistent chat storage with SQLite

### ✅ Performance

- **Fast Inference** - 150+ tokens/sec (vs 0.4 tokens/sec with PyTorch)
- **Optimized Model** - GGUF quantization for minimal memory usage
- **Hot Reload** - Instant frontend updates during development

### ✅ User Experience

- **Authentication** - Secure JWT-based login/logout
- **Demo Mode** - Automatic fallback to demo user for presentations
- **Responsive UI** - Works on desktop and mobile
- **Dark Mode** - Modern, eye-friendly interface

---

## 🛠️ Development Tools

### Version Control

- **Git** - Source code management

### Package Managers

- **npm/pnpm** - Frontend dependencies
- **pip** - Python package management

### Code Quality

- **TypeScript** - Type safety in frontend
- **Pydantic** - Runtime validation in backend
- **ESLint** (likely) - JavaScript/TypeScript linting

---

## 📁 Project Structure

```
ai_backend/
├── app/                    # Backend API
│   ├── api.py             # FastAPI routes
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   ├── auth.py            # JWT authentication
│   ├── ml_engine_lmstudio.py  # LM Studio integration
│   └── database.py        # Database configuration
├── frontend/              # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── contexts/      # React Context providers
│   │   └── lib/           # Utilities
│   ├── public/            # Static assets
│   └── package.json
├── main.py                # Backend entry point
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

---

## 🌐 Environment & Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend Dev Server | 5173 | <http://localhost:5173> |
| Backend API | 8080 | <http://localhost:8080> |
| LM Studio API | 1234 | <http://localhost:1234> |

---

## 🔒 Security Features

- **Password Hashing** - bcrypt with configurable rounds
- **JWT Tokens** - Signed with secret key
- **HTTPOnly Cookies** - Prevents XSS attacks
- **CORS Configuration** - Controlled cross-origin requests
- **Parameterized Queries** - SQL injection prevention (SQLAlchemy)

---

## 📊 Performance Metrics

| Metric | Before (PyTorch) | After (LM Studio) | Improvement |
|--------|------------------|-------------------|-------------|
| Inference Speed | 0.4 tokens/sec | 150+ tokens/sec | **375x faster** |
| Response Time | 8+ minutes | 2-3 seconds | **160x faster** |
| Memory Usage | ~8GB VRAM | ~2GB VRAM | **4x less** |
| Model Size | 3.1GB (FP16) | 900MB (Q4_K_M) | **3.4x smaller** |

---

## 🎯 Use Cases

1. **ESG Report Analysis** - Automated sustainability reporting
2. **Financial Document Review** - Quick insights from annual reports
3. **Compliance Checking** - Governance and regulatory analysis
4. **Sustainability Metrics** - Environmental impact assessment
5. **Corporate Social Responsibility** - Social initiative evaluation

---

## 📝 Notes

- **Authentication**: Flexible mode for demos (auto-login as demo user)
- **Model**: Custom fine-tuned for ESG domain
- **Deployment**: Designed for local development; production deployment requires configuration
- **Scalability**: SQLite suitable for demo; consider PostgreSQL for production

---

**Built with ❤️ for ESG Analysis**

*Last Updated: December 2025*
