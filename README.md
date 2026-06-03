# 🦊 Email_Agent - AI-Powered Email Assistant

An intelligent email management system that uses AI to help you summarize and reply to emails with ease. Email_Agent combines Gmail API integration with local LLM capabilities (via Ollama) to provide a seamless email assistance experience.

## Features

✨ **Core Features:**
- 📥 **Gmail Integration** - Fetch unread emails directly from your Gmail inbox
- 🧠 **AI Summarization** - Get concise 3-5 bullet point summaries of email content
- ✍️ **AI Reply Generation** - Generate professional replies to emails automatically
- 🎨 **User-Friendly Interface** - Clean Streamlit-based web UI
- ⚡ **Local AI Processing** - Uses Ollama with Llama 3.2 for privacy and speed
- 🔒 **CORS Support** - Secure backend with CORS middleware for frontend communication

## Architecture

```
Email_Agent/
├── backend/
│   ├── main.py              # FastAPI server with Gmail API & Ollama integration
│   └── requirements.txt      # Python dependencies
├── frontend/
│   └── app.py               # Streamlit UI application
└── README.md
```

### Backend Stack
- **FastAPI** - Modern async web framework
- **Gmail API** - Official Google Gmail integration
- **Ollama** - Local LLM backend
- **BeautifulSoup** - HTML parsing for email bodies
- **Pydantic** - Data validation

### Frontend Stack
- **Streamlit** - Interactive Python web app framework
- **Requests** - HTTP client for backend communication

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.8+** installed
2. **Ollama** installed and running locally
3. **Google Account** with Gmail enabled
4. **Google Cloud Project** with Gmail API enabled

### Setup Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API
4. Create OAuth 2.0 Desktop Application credentials
5. Download the credentials and save as `backend/credentials.json`

### Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai)

Pull the required model:
```bash
ollama pull llama3.2:1b
```

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/om3341/Email_Agent.git
cd Email_Agent
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Place your `credentials.json` file in the `backend/` directory**

### 3. Setup Frontend

```bash
cd frontend

# Create virtual environment (optional, can reuse backend venv)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Streamlit and requests
pip install streamlit requests
```

## Running the Application

### Start Ollama Service
```bash
ollama serve
```
The service will run on `http://localhost:11434`

### Start Backend Server

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload
```
Backend will be available at `http://localhost:8000`

### Start Frontend Application

In a new terminal:
```bash
cd frontend
source venv/bin/activate  # or venv\Scripts\activate on Windows
streamlit run app.py
```
Frontend will open at `http://localhost:8501`

## Usage

1. **Load Inbox** - Click the "🔄 Load Inbox" button to fetch your unread Gmail messages
2. **Select Email** - Click on any email in the inbox list to view it in detail
3. **Summarize** - Click "📝 Summarize Email" to generate AI bullet points
4. **Generate Reply** - Click "✍️ Generate Reply" to get an AI-generated professional response

## API Endpoints

### Backend Endpoints

#### GET `/gmail/inbox`
Fetch unread emails from Gmail inbox.

**Response:**
```json
{
  "success": true,
  "emails": [
    {
      "id": "msg-id",
      "from": "sender@example.com",
      "subject": "Email Subject",
      "body": "Email content..."
    }
  ]
}
```

#### POST `/summarize`
Summarize email content.

**Request:**
```json
{
  "email_text": "Email body content..."
}
```

**Response:**
```json
{
  "success": true,
  "summary": "- Point 1\n- Point 2\n- Point 3"
}
```

#### POST `/reply`
Generate a professional reply to an email.

**Request:**
```json
{
  "email_text": "Email body content..."
}
```

**Response:**
```json
{
  "success": true,
  "reply": "Dear sender,\n\nThank you for your email..."
}
```

## Configuration

### Backend Configuration (main.py)

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama API endpoint |
| `MODEL_NAME` | `llama3.2:1b` | LLM model to use |
| `SCOPES` | `["https://www.googleapis.com/auth/gmail.readonly"]` | Gmail API scopes |

### Frontend Configuration (app.py)

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_URL` | `http://127.0.0.1:8000` | Backend server URL |

## Security Notes

⚠️ **Important:**
- Never commit `credentials.json` or `token.json` to version control
- Keep your `.gitignore` updated to exclude sensitive files
- The application uses Gmail read-only scope - it cannot send or delete emails
- Ollama runs locally, ensuring email privacy

## Troubleshooting

### "⚠️ AI service unavailable"
- Ensure Ollama is running: `ollama serve`
- Check that the model is installed: `ollama list`
- Verify `OLLAMA_URL` in `backend/main.py`

### "❌ Backend not reachable"
- Ensure backend server is running
- Check that `BACKEND_URL` in `frontend/app.py` matches backend address
- Verify no port conflicts on localhost:8000

### "❌ Failed to connect to Gmail"
- Verify `credentials.json` is in the `backend/` directory
- Check Gmail API is enabled in Google Cloud Console
- Re-authenticate: delete `token.json` and restart backend

### Email body showing as "No readable text found"
- The email may be in an unsupported format
- Try a different email or check email encoding

## Requirements

See `backend/requirements.txt` for full dependencies:
- FastAPI 0.123.8
- Google API Client libraries
- BeautifulSoup4
- Ollama Python client
- Pydantic 2.12.5
- Uvicorn 0.38.0

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source. Feel free to use, modify, and distribute.

## Future Enhancements

🚀 Potential improvements:
- Email search and filtering
- Draft saving functionality
- Support for other email providers
- Advanced AI models integration
- Email scheduling
- Bulk operations
- Multi-language support

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ by om3341**