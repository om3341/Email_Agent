from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import base64
from bs4 import BeautifulSoup
import os
import re

# ---------------------------
# FastAPI Setup
# ---------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# OLLAMA CONFIG
# ---------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

class EmailRequest(BaseModel):
    email_text: str

def ask_ollama(prompt: str) -> str:
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if response.status_code != 200:
            return "⚠️ AI service unavailable."
        return response.json().get("response", "").strip()
    except Exception:
        return "⚠️ Failed to connect to AI engine."

@app.post("/summarize")
def summarize(req: EmailRequest):
    text = req.email_text[:4000]
    prompt = f"Summarize this email in 3-5 clean bullet points:\n\n{text}"
    return {"success": True, "summary": ask_ollama(prompt)}

@app.post("/reply")
def reply(req: EmailRequest):
    text = req.email_text[:4000]
    prompt = f"Write a polite and professional reply to this email:\n\n{text}"
    return {"success": True, "reply": ask_ollama(prompt)}

# ---------------------------
# GMAIL API
# ---------------------------

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

# ---------------------------
# EMAIL BODY CLEANER
# ---------------------------

def extract_clean_body(payload):
    def walk(part):
        if part.get("parts"):
            for p in part["parts"]:
                r = walk(p)
                if r:
                    return r

        mime = part.get("mimeType")
        data = part.get("body", {}).get("data")

        if not data:
            return None

        decoded = base64.urlsafe_b64decode(data).decode(errors="ignore")

        if mime == "text/plain":
            return decoded

        if mime == "text/html":
            soup = BeautifulSoup(decoded, "html.parser")
            return soup.get_text(separator="\n", strip=True)

        return None

    raw = walk(payload)
    if not raw:
        return "No readable text found."

    raw = raw.encode("utf-8").decode("unicode_escape", errors="ignore")
    raw = re.sub(r"http[s]?://\S+", "", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)

    return raw.strip()

# ---------------------------
# FETCH GMAIL INBOX (SAFE)
# ---------------------------

@app.get("/gmail/inbox")
def get_inbox():
    try:
        service = get_gmail_service()

        results = service.users().messages().list(
            userId="me", q="is:unread", maxResults=10
        ).execute()

        messages = results.get("messages", [])
        inbox = []

        for msg in messages:
            email = service.users().messages().get(
                userId="me", id=msg["id"], format="full"
            ).execute()

            payload = email.get("payload", {})
            headers = payload.get("headers", [])

            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "")

            body = extract_clean_body(payload)

            inbox.append({
                "id": msg["id"],
                "from": sender,
                "subject": subject,
                "body": body
            })

        return {"success": True, "emails": inbox}

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
