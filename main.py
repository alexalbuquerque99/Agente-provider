import os
from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()

# O Railway injeta a chave aqui automaticamente via Variáveis de Ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    user_id: str
    message: str

SYSTEM_PROMPT = """
Você é o técnico de suporte da S L Albuquerque Telecom.
Seu objetivo é ser prático.
1. Se o cliente disser 'estou sem internet', peça para reiniciar o roteador (30 seg fora da tomada).
2. Se não resolver, diga que um atendente humano foi notificado.
3. Não fale de preços.
"""

@app.get("/")
def home():
    return {"status": "Agente Online"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"response": "Erro técnico, tente reiniciar seu modem."}