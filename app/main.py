# app/main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from app.gemini_client import client

# Cargar variables desde .env
load_dotenv()

app = FastAPI(title="ChatBot IA - FastAPI + Gemini")

class ChatRequest(BaseModel):
    message: str
    mode: str = "brief"   # "brief" o "extended"

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        # Prompt dinámico según modo
        if req.mode == "brief":
            contents = f"Responde en 2-3 frases a la pregunta: {req.message}"
            model = "gemini-2.5-flash"
        else:
            contents = (
                "Proporciona una respuesta extendida, con explicaciones y, cuando sea posible, "
                "incluye citas o referencias: " + req.message
            )
            model = "gemini-2.5-flash"

        # Llamada al modelo Gemini
        response = client.models.generate_content(
            model=model,
            contents=contents
        )

        return {"answer": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
