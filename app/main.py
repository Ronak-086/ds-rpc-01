from fastapi import FastAPI, Form
from app.services.rag_service import RagService

app = FastAPI()
rag_service = RagService()

@app.post("/chat")
def chat(message: str = Form(...), role: str = Form(...)):
    answer = rag_service.ask(message, role)
    return {"response": answer}
