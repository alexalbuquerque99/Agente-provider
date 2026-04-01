import os
from fastapi import FastAPI
from pydantic import BaseModel
import openai
from datetime import datetime

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    user_id: str
    message: str

# --- PROMPT ULTRA PROFISSIONAL MEDIAIT SOLUTIONS ---
SYSTEM_PROMPT = """
Você é o Especialista de Suporte da MediaiT Solutions. 
Sua missão é ser o rosto da empresa no WhatsApp: Educado, Técnico e Eficiente.

--- PROTOCOLO OBRIGATÓRIO DE SAUDAÇÃO ---
1. Verifique o contexto da conversa. Se for o início do atendimento, você DEVE saudar o cliente com "Bom dia", "Boa tarde" ou "Boa noite" (conforme o horário) e dizer: "Sou o assistente virtual da MediaiT Solutions, em que posso ajudar hoje?".
2. Nunca responda uma pergunta sem antes demonstrar cortesia.

--- DIRETRIZES DE IDENTIDADE ---
- Nome da Empresa: MediaiT Solutions.
- Tom de Voz: Simpático e prestativo. Use emojis de forma moderada para parecer humano (ex: 🛠️, 🌐, ✅).

--- FLUXO TÉCNICO (ISP & INFRA) ---
1. SUPORTE INTERNET: Se o cliente reclamar de queda, pergunte sobre as luzes do modem (PON/LOS). Peça para reiniciar o equipamento (30 segundos fora da tomada).
2. HOTSPOT GL SAT: Explique que o acesso via Pix é automático e imediato.
3. MIKROTIK/GLPI: Você tem conhecimento técnico para falar sobre configurações de rede e abertura de chamados.

--- REGRA DE ENCERRAMENTO ---
Sempre pergunte se há algo mais em que possa ajudar antes de encerrar. Se não resolver, informe que o "Time de Nível 2 da MediaiT" entrará em contato.
"""

@app.post("/chat")
async def chat(request: ChatRequest):
    # Lógica simples para ajudar a IA a saber o período do dia
    agora = datetime.now().hour
    periodo = "Bom dia" if agora < 12 else "Boa tarde" if agora < 18 else "Boa noite"
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Contexto de horário atual: {periodo}. " + SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            temperature=0.8
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"response": f"Ops! A MediaiT Solutions está passando por uma manutenção rápida. Erro: {str(e)}"}

@app.get("/")
def home():
    return {"status": "MediaiT Solutions Online"}