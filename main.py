import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from datetime import datetime

app = FastAPI()

# Pega a chave da variável de ambiente do Railway
# Certifique-se que no Railway a variável se chama GROQ_API_KEY
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    user_id: str
    message: str

SYSTEM_PROMPT = """
Você é o Especialista de Suporte da MediaiT Solutions. 
Sua missão é ser o rosto da empresa no WhatsApp: Educado, Técnico e Eficiente.

--- PROTOCOLO OBRIGATÓRIO DE SAUDAÇÃO ---
1. Se for o início do atendimento, você DEVE saudar o cliente com "Bom dia", "Boa tarde" ou "Boa noite" (conforme o horário) e dizer: "Sou o assistente virtual da MediaiT Solutions, em que posso ajudar hoje?".
2. Seja sempre cordial e use emojis moderadamente (ex: 🛠️, 🌐).

--- CONTEXTO TÉCNICO ---
- Nome: MediaiT Solutions.
- Especialidade: Internet Fibra, MikroTik, Hotspot GL Sat e GLPI 10.
- Procedimento: Sempre sugira o "Power Cycle" (30s fora da tomada) para problemas de conexão.
"""

@app.post("/chat")
async def chat(request: ChatRequest):
    agora = datetime.now().hour
    periodo = "Bom dia" if agora < 12 else "Boa tarde" if agora < 18 else "Boa noite"
    
    try:
        # Usando o modelo Llama 3 da Groq (Muito mais rápido)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"Horário atual: {periodo}. " + SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            model="llama3-8b-8192",
        )
        return {"response": chat_completion.choices[0].message.content}
    except Exception as e:
        # Se der erro aqui, ele vai mostrar se é a CHAVE ou Conexão
        return {"response": f"Erro técnico na MediaiT: {str(e)}"}

@app.get("/")
def home():
    return {"status": "MediaiT Solutions Online via Groq"}