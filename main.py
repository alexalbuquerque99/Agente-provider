import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq  # Mudamos de OpenAI para Groq
from datetime import datetime

app = FastAPI()

# No Railway, altere o nome da variável de ambiente para GROQ_API_KEY
# Ou apenas garanta que o valor da chave gsk_... esteja aqui
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    user_id: str
    message: str

SYSTEM_PROMPT = """
Você é o Especialista de Suporte da MediaiT Solutions. 
Sua missão é ser o rosto da empresa no WhatsApp: Educado, Técnico e Eficiente.

--- PROTOCOLO OBRIGATÓRIO DE SAUDAÇÃO ---
1. Se for o início do atendimento, você DEVE saudar o cliente com "Bom dia", "Boa tarde" ou "Boa noite" e dizer: "Sou o assistente virtual da MediaiT Solutions, em que posso ajudar hoje?".
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
        # Chamada específica para a API da Groq (Llama 3 ou Mixtral)
        response = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=[
                {"role": "system", "content": f"Horário: {periodo}. " + SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"response": f"Ops! A MediaiT Solutions detectou um erro técnico: {str(e)}"}

@app.get("/")
def home():
    return {"status": "MediaiT Solutions Online via Groq"}