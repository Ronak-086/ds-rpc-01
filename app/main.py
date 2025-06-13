from typing import Dict
from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()
from fastapi import Form
from app.services.rag_service import RagService

rag_service = RagService()
# Dummy user database (fixed the typo in 'Natasha')
users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"},
    "Clark": {"password": "employee123", "role": "employee"},
    "Steve": {"password": "c123", "role": "c_level"}
}

# Authentication dependency
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}

@app.get("/")
def root():
    return {"message": "RBAC Chatbot API is running"}

# Login endpoint
@app.get("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


# Protected test endpoint
@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}


# Protected chat endpoint (RAG to be implemented later)
@app.post("/chat")
def query(user=Depends(authenticate), message: str = Form(...)):
    response = rag_service.ask(message, user['role'])
    return {
        "username": user['username'],
        "role": user['role'],
        "response": response
    }
