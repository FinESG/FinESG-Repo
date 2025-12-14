# ESG Reporter 🌱

AI-powered ESG (Environmental, Social, Governance) analysis and reporting platform using a fine-tuned language model.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 👥 Team

This project was developed by:

- **[Ansh S](https://github.com/Anshs-12)**
- **[Ananya](https://github.com/ananya-gh-05)**
- **[Anshita](https://github.com/Anshitas-12)**
- **[Deepak J](https://github.com/jdeepak1218)**
- **[Shriya](https://github.com/Shriya-1206)**

## 📄 Research Paper

**[Read our research paper →](https://github.com/FinESG/research-paper)**

*AI-Powered ESG Analysis using Fine-Tuned Language Models*

## ✨ Features

- 🤖 **AI-Powered Analysis** - ESG-specialized language model (fingesg4)
- 📄 **PDF Upload** - Analyze annual reports and financial documents
- 💬 **Chat Interface** - Multi-turn conversations with context awareness
- 🔐 **Secure Authentication** - JWT-based login with demo mode
- 💾 **Persistent Storage** - SQLite database for conversation history
- ⚡ **Fast Inference** - 150+ tokens/sec using LM Studio

## 🚀 Quick Start

### Prerequisites

- **Python** 3.10+
- **Node.js** 18+
- **LM Studio** (for AI model serving)
- **Git**

### 1. Clone Repository

```bash
git clone <repository-url>
cd ai_backend
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run backend server
python main.py
```

Backend will start on **<http://localhost:8080>**

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start on **<http://localhost:5173>**

### 4. LM Studio Setup & fingesg4 Model

#### Option A: Quick Start (Use Base Model)

1. **Download & Install** [LM Studio](https://lmstudio.ai/)
2. **Download Model**: Search for "Qwen 2.5-1.5B-Instruct" in LM Studio
3. **Load Model** in Chat tab
4. **Start Local Server** on port 1234

#### Option B: Use Fine-Tuned ESG Model (Recommended)

##### Step 1: Download fingesg4 Model

**Download our pre-converted GGUF model:**

📥 **[Download fingesg4.gguf from Google Drive](https://drive.google.com/file/d/1fe995X-uJfJCgHq48QltGuukWTxrw9q8/view?usp=sharing)** (~3.1GB)

> **Note**: This is our custom ESG-specialized model, fine-tuned on financial and sustainability reporting data.

##### Step 2: Import to LM Studio (CRITICAL: Folder Structure)**

LM Studio requires a **double-nested folder structure**:

```
C:\Users\<YourName>\.lmstudio\models\
└── fingesg4\              # Parent folder
    └── fingesg4\          # Child folder (same name!)
        └── fingesg4.gguf  # Your model file
```

**Manual Setup:**

```bash
# Navigate to LM Studio models directory
cd "C:\Users\<YourName>\.lmstudio\models"

# Create parent folder
mkdir fingesg4

# Create child folder (same name)
mkdir fingesg4\fingesg4

# Copy your GGUF file into the nested folder
copy "C:\path\to\llama.cpp\fingesg4.gguf" "fingesg4\fingesg4\fingesg4.gguf"
```

**Step 3: Load in LM Studio**

1. **Restart LM Studio** completely (close and reopen)
2. **Go to "My Models" tab** - you should now see `fingesg4`
3. **Click "Chat" tab** → Select `fingesg4` from dropdown
4. **Go to "Local Server" tab** → Click "Start Server" (port 1234)
5. **Verify**: Status should show "Running" with model name `fingesg4`

> **Troubleshooting**: If model doesn't appear, verify the folder structure is exactly: `models\fingesg4\fingesg4\fingesg4.gguf`

## 📋 Tech Stack

### Frontend

- **React** 18 + TypeScript
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library

### Backend

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database
- **Pydantic** - Validation

### AI/ML

- **LM Studio** - Model serving
- **fingesg4** - ESG-specialized model
- **Qwen 2.5-1.5B** - Base model

See [TECH_STACK.md](./TECH_STACK.md) for complete details.

## 📁 Project Structure

```
ai_backend/
├── app/                    # Backend (FastAPI)
│   ├── api.py             # API routes
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   ├── auth.py            # Authentication
│   └── ml_engine_lmstudio.py  # LM Studio integration
├── frontend/              # Frontend (React)
│   ├── src/
│   │   ├── components/    # React components
│   │   └── contexts/      # State management
│   └── package.json
├── main.py                # Backend entry point
├── requirements.txt       # Python dependencies
└── README.md
```

## 🔧 Configuration

### Environment Variables (Optional)

Create `.env` file in root:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./ai_backend.db
```

### Default Credentials (Demo Mode)

- **Email**: <demo@example.com>
- **Password**: demo123

## 📊 Performance

| Metric | Value |
|--------|-------|
| Inference Speed | 150+ tokens/sec |
| Response Time | 2-3 seconds |
| Memory Usage | ~2GB VRAM |
| Model Size | 900MB (quantized) |

## 🎯 Use Cases

- ESG report analysis
- Sustainability reporting
- Financial document review
- Compliance checking
- Corporate governance analysis

## 🛡️ Security

- JWT token authentication
- HTTPOnly cookies
- Password hashing (bcrypt)
- Parameterized SQL queries
- CORS configuration

## 📝 API Documentation

Once the backend is running, visit:

- **Swagger UI**: <http://localhost:8080/docs>
- **ReDoc**: <http://localhost:8080/redoc>

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Acknowledgments

- **Qwen Team** - Base language model
- **LM Studio** - Optimized inference engine
- **FastAPI** - Modern Python web framework
- **shadcn/ui** - Beautiful component library

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for ESG Analysis**

*Making sustainability reporting accessible and efficient*
