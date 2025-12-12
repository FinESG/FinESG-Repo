# ESG Reporter 🌱

AI-powered ESG (Environmental, Social, Governance) analysis and reporting platform using a fine-tuned language model.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

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

**Step 1: Convert fingesg4 Model to GGUF**

```bash
# Install dependencies
pip install transformers peft accelerate

# Run merge script (creates fingesg4_merged folder)
python merge_fingesg4.py

# Clone llama.cpp for conversion
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# Convert to GGUF format
python convert_hf_to_gguf.py ../fingesg4_merged --outtype f16 --outfile fingesg4.gguf
```

> **Note**: The `merge_fingesg4.py` script downloads the fingesg4 adapter from [HuggingFace](https://huggingface.co/DeepakJ1218/fingesg4) and merges it with Qwen 2.5-1.5B base model.

**Step 2: Import to LM Studio (CRITICAL: Folder Structure)**

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

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Qwen Team** - Base language model
- **LM Studio** - Optimized inference engine
- **FastAPI** - Modern Python web framework
- **shadcn/ui** - Beautiful component library

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for ESG Analysis**

*Making sustainability reporting accessible and efficient*
