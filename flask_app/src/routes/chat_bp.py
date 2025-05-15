# Este arquivo define o blueprint para as rotas de chat.
import asyncio
from flask import Blueprint, request, jsonify
import httpx # Para chamadas HTTP assíncronas ao LLM

chat_bp = Blueprint("chat_bp", __name__)

# Configuração (idealmente viria de um arquivo de configuração ou variáveis de ambiente)
LLM_API_URL = "YOUR_LLM_API_ENDPOINT_HERE"  # Substitua pelo endpoint real da API do LLM
LLM_API_KEY = "YOUR_LLM_API_KEY_HERE"      # Substitua pela sua chave de API, se necessário

async def get_llm_response(user_message: str):
    """Função assíncrona para obter resposta do LLM."""
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gemini-2.0-flash", # Exemplo, pode ser configurável
        "contents": [{
            "parts": [{
                "text": user_message
            }]
        }]
        # Adapte o payload conforme a API do seu LLM (Gemini, OpenAI, etc.)
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client: # Timeout de 60 segundos
            response = await client.post(LLM_API_URL, json=payload, headers=headers)
            response.raise_for_status()  # Lança exceção para respostas de erro HTTP (4xx ou 5xx)
            llm_data = response.json()
            # Extraia a resposta do LLM da estrutura de dados retornada pela API
            # Isto é um exemplo e precisará ser ajustado para a API específica do Gemini 2.0 Flash
            if llm_data.get("candidates") and llm_data["candidates"][0].get("content"): 
                return llm_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                # Fallback ou log de erro se a estrutura da resposta não for a esperada
                print(f"Resposta inesperada do LLM: {llm_data}")
                return "Desculpe, não consegui processar a resposta do modelo no momento."
    except httpx.HTTPStatusError as e:
        print(f"Erro HTTP ao chamar LLM API: {e.response.status_code} - {e.response.text}")
        return f"Erro ao comunicar com o modelo: {e.response.status_code}"
    except httpx.RequestError as e:
        print(f"Erro de requisição ao chamar LLM API: {e}")
        return "Erro de conexão ao tentar comunicar com o modelo."
    except Exception as e:
        print(f"Erro inesperado ao processar resposta do LLM: {e}")
        return "Ocorreu um erro inesperado ao processar sua solicitação."

@chat_bp.route("/chat", methods=["POST"])
async def handle_chat():
    """Endpoint assíncrono para o chat."""
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Mensagem não fornecida"}), 400

    user_message = data["message"]

    # Chama a função assíncrona para obter a resposta do LLM
    try:
        bot_response = await get_llm_response(user_message)
        return jsonify({"reply": bot_response})
    except Exception as e:
        print(f"Erro no endpoint /chat: {e}")
        return jsonify({"error": "Erro interno ao processar a mensagem"}), 500

# Exemplo de uma rota síncrona para demonstrar que ambas podem coexistir
@chat_bp.route("/health_check", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200

