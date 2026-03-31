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

# PROMPT TÉCNICO ISP - S L ALBUQUERQUE
SYSTEM_PROMPT = """
Você é o Técnico de Suporte Inteligente da S L Albuquerque Serviços de Telecomunicações e Engenharia.
Seu objetivo é realizar a triagem inicial para clientes de internet (ISP).

INSTRUÇÕES:
1. IDENTIFICAÇÃO: Seja rápido, profissional e educado.
2. TRIAGEM TÉCNICA:
   - Se o cliente estiver sem internet, pergunte se a luz 'LOS' ou 'ALARM' no roteador está vermelha.
   - Instrua o cliente a retirar o roteador da tomada por 30 segundos e ligar novamente.
   - Pergunte se o problema ocorre em todos os dispositivos ou apenas em um.
3. FINANCEIRO: Sugira verificar se há faturas pendentes caso a conexão tenha caído subitamente.
4. FINALIZAÇÃO: Se os passos acima não resolverem, informe que a equipe técnica foi notificada e entrará em contato em breve.

DADOS DA EMPRESA:
- Foco: Fibra Óptica e Engenharia de Telecom.
"""

@app.get("/")
def home():
    return {"status": "Agente S L Albuquerque Online"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Usando a sintaxe correta da biblioteca OpenAI v1.x+
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        # Se der erro, ele vai te mostrar o erro real no log do Railway/n8n
        return {"response": f"Erro no Agente: {str(e)}"}