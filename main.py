import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from datetime import datetime

app = FastAPI()

# Configuração Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    user_id: str
    message: str

SYSTEM_PROMPT = """
Você é o Especialista de Suporte da MediaiT Solutions. 
Sua missão é ser o rosto da empresa no WhatsApp: Educado, Técnico e Eficiente.

--- PROTOCOLO OBRIGATÓRIO DE SAUDAÇÃO ---
1. Sempre saude o cliente com "Bom dia", "Boa tarde" ou "Boa noite".
2. Identifique-se: "Sou o assistente virtual da MediaiT Solutions, em que posso ajudar?".
3. Seja sempre cordial e use emojis (🛠️, 🌐).

--- CONTEXTO TÉCNICO ---
- Nome: MediaiT Solutions.
- Especialidade: Internet Fibra, MikroTik, Hotspot GL Sat.
"""

@app.post("/chat")
async def chat(request: ChatRequest):
    # Horário simplificado sem pytz
    hora = datetime.now().hour
    periodo = "Bom dia" if hora < 12 else "Boa tarde" if hora < 18 else "Boa noite"
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"Contexto: {periodo}. " + SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"response": f"Erro técnico na MediaiT: {str(e)}"}

@app.get("/")
def home():
    return {"status": "MediaiT Online"}