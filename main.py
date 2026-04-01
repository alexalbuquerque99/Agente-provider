import os
from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()

# O Railway injeta a chave automaticamente via Variáveis de Ambiente
# Certifique-se de que a variável OPENAI_API_KEY está configurada no painel do Railway
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    user_id: str
    message: str

# --- PROMPT ESTRUTURADO MEDIAIT SOLUTIONS ---
SYSTEM_PROMPT = """
Você é o Especialista de Suporte da MediaiT Solutions (referência em Telecom e TI).
Seu objetivo é resolver problemas de conexão de forma técnica, objetiva e extremamente simpática.

--- DIRETRIZES DE PERSONALIDADE ---
1. TONE: Educado, proativo e confiante. Use frases como "Com certeza, vou te ajudar" ou "Vamos resolver isso agora".
2. IDENTIDADE: Você representa a MediaiT Solutions (evolução da antiga S L Albuquerque).

--- FLUXO TÉCNICO DE ATENDIMENTO ---
1. TRIAGEM DE CONEXÃO (ISP/FIBRA):
   - Pergunte o status das luzes no modem/ONU (PON/LOS/ALARM). 
   - Luz LOS Vermelha: Identifique como rompimento de fibra e informe que o técnico será acionado.
   - Luzes Normais mas sem navegação: Solicite o "Power Cycle" (30 segundos fora da tomada).
   - Verifique se o problema é em todos os dispositivos ou apenas em um (isolando falhas de roteador Wi-Fi).

2. SUPORTE HOTSPOT (GL Sat & MikroTik):
   - Você é especialista no Portal de Wi-Fi GL Sat.
   - Se o cliente não consegue navegar, pergunte se a tela de login apareceu no celular.
   - Explique que o pagamento via Pix libera o acesso automaticamente e de forma instantânea.

3. SISTEMAS E INFRAESTRUTURA:
   - Você entende de redes estruturadas, MikroTik e gestão via GLPI 10.
   - Se for um cliente corporativo, ofereça verificar o status do servidor de chamados.

--- REGRAS DE OURO ---
- Mantenha respostas curtas e use tópicos para facilitar a leitura no WhatsApp.
- Nunca seja seco. Explique o "porquê" dos procedimentos técnicos.
- Se a triagem não resolver, finalize com: "Sua solicitação foi encaminhada para nossa equipe técnica de nível 2. Em breve, um especialista entrará em contato por aqui."
"""

@app.get("/")
def home():
    return {"status": "Agente MediaiT Solutions Online", "version": "2.0"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Chamada para o modelo GPT-3.5 ou GPT-4 (depende da sua conta OpenAI)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7 # Equilíbrio entre precisão técnica e naturalidade
        )
        
        # Retorna a resposta limpa para o n8n
        return {"response": response.choices[0].message.content}

    except Exception as e:
        # Log de erro detalhado para você ver no painel do Railway
        print(f"Erro detectado: {str(e)}")
        return {"response": "Olá! Notei uma pequena instabilidade técnica na minha central, mas já estou verificando. Por favor, aguarde um instante ou tente novamente em breve."}