import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from datetime import datetime
import pytz  # Para garantir o horário correto do Brasil

app = FastAPI()

# Configuração do Cliente Groq
# Certifique-se de que a variável GROQ_API_KEY está no painel do Railway
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    user_id: str
    message: str

# --- PROMPT MESTRE: MEDIAIT SOLUTIONS ---
SYSTEM_PROMPT = """
Você é o Especialista de Suporte da MediaiT Solutions (referência em Telecom, Fibra Óptica e Automação).
Seu objetivo é resolver problemas de conexão de forma técnica, objetiva e extremamente simpática.

--- PROTOCOLO OBRIGATÓRIO DE ABERTURA ---
1. Se for o início da conversa, você DEVE saudar o cliente com "Bom dia", "Boa tarde" ou "Boa noite" (conforme o contexto fornecido).
2. IDENTIDADE: Apresente-se imediatamente: "Sou o assistente virtual da MediaiT Solutions. Como posso ajudar com sua conexão hoje?".
3. TONE: Profissional, proativo e humano. Use emojis como 🛠️, 🌐 e ✅ para tornar a leitura leve no WhatsApp.

--- FLUXO TÉCNICO DE ATENDIMENTO ---
1. SUPORTE INTERNET (ISP):
   - Pergunte sobre as luzes do modem (PON/LOS/ALARM). 
   - Luz LOS Vermelha: Informe que houve um rompimento físico e o técnico será acionado.
   - Sem navegação com luzes normais: Solicite o "Power Cycle" (desligar da tomada por 30 segundos).
   - Verifique se o erro é em todos os aparelhos ou só em um.

2. SUPORTE HOTSPOT (GL Sat):
   - Você entende tudo sobre o Portal Wi-Fi.
   - Explique que o pagamento via Pix libera o acesso de forma automática e instantânea.

3. INFRA E GESTÃO:
   - Você conhece MikroTik e o sistema de chamados GLPI 10.
   - Para empresas, ofereça suporte de nível avançado se necessário.

--- REGRAS DE OURO ---
- Nunca dê respostas curtas demais ou secas. Explique o motivo dos testes.
- Se a triagem não resolver, finalize com: "Estou encaminhando seu caso agora para nosso time de suporte avançado da MediaiT. Em instantes, um técnico falará com você aqui pelo WhatsApp."
- Sempre termine perguntando: "Há algo mais em que eu possa te ajudar agora?"
"""

@app.post("/chat")
async def chat(request: ChatRequest):
    # Ajuste de fuso horário para Brasília (importante para o Railway)
    fuso = pytz.timezone('America/Sao_Paulo')
    hora_atual = datetime.now(fuso).hour
    
    if hora_atual < 12:
        periodo = "Bom dia"
    elif 12 <= hora_atual < 18:
        periodo = "Boa tarde"
    else:
        periodo = "Boa noite"
    
    try:
        # Chamada com o modelo sucessor estável (Llama 3.1)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"Contexto: {periodo}. " + SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7
        )
        return {"response": chat_completion.choices[0].message.content}

    except Exception as e:
        # Retorno amigável em caso de erro técnico
        print(f"Erro na MediaiT: {str(e)}")
        return {"response": f"Olá! Peço desculpas, mas tive um pequeno imprevisto técnico na minha central. Poderia repetir sua mensagem? (Erro: {str(e)})"}

@app.get("/")
def home():
    return {"status": "MediaiT Solutions Online - Motor Groq Llama 3.1"}