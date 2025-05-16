import asyncio
from flask import Blueprint, request, jsonify
import httpx # Para chamadas HTTP assíncronas ao LLM

chat_bp = Blueprint("chat_bp", __name__)

# Configuração (idealmente viria de um arquivo de configuração ou variáveis de ambiente)
LLM_API_URL = "YOUR_LLM_API_ENDPOINT_HERE"  # Substitua pelo endpoint real da API do LLM
LLM_API_KEY = "YOUR_LLM_API_KEY_HERE"      # Substitua pela sua chave de API, se necessário

async def get_llm_response(user_message: str):
    """Função assíncrona para obter resposta do LLM com tratamento de resposta aprimorado."""
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    # Payload para a API Gemini. Adapte conforme a documentação específica do modelo.
    # Este payload é comum para modelos de geração de texto.
    payload = {
        "contents": [{
            "parts": [{
                "text": user_message
            }]
        }],
        # Configurações adicionais podem ser necessárias dependendo do modelo/API,
        # como "generationConfig": {"candidateCount": 1} para garantir um candidato,
        # ou especificações de segurança, etc.
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client: # Timeout de 60 segundos
            response = await client.post(LLM_API_URL, json=payload, headers=headers)
            response.raise_for_status()  # Lança exceção para respostas de erro HTTP (4xx ou 5xx)
            llm_data = response.json()

            # Extração robusta da resposta de texto da API Gemini
            try:
                # Verifica se 'candidates' existe e é uma lista não vazia
                if llm_data.get("candidates") and isinstance(llm_data["candidates"], list) and llm_data["candidates"]:
                    candidate = llm_data["candidates"][0]
                    # Verifica se 'content' existe no candidato
                    if candidate.get("content") and isinstance(candidate["content"], dict):
                        content = candidate["content"]
                        # Verifica se 'parts' existe no conteúdo e é uma lista não vazia
                        if content.get("parts") and isinstance(content["parts"], list) and content["parts"]:
                            part = content["parts"][0]
                            # Verifica se 'text' existe na parte e é uma string
                            if part.get("text") and isinstance(part["text"], str):
                                return part["text"]
                
                # Se a estrutura esperada não for encontrada ou o texto estiver ausente
                print(f"Resposta do LLM com estrutura inesperada ou sem texto: {llm_data}")
                return "Desculpe, não consegui extrair uma resposta de texto válida do modelo no momento."

            except Exception as e_parser: # Captura exceções durante o parsing da resposta
                print(f"Erro ao analisar a estrutura da resposta do LLM: {e_parser}. Resposta recebida: {llm_data}")
                return "Erro ao processar a estrutura da resposta do modelo."

    except httpx.HTTPStatusError as e:
        print(f"Erro HTTP ao chamar LLM API: {e.response.status_code} - {e.response.text}")
        return f"Erro ao comunicar com o modelo: {e.response.status_code}"
    except httpx.RequestError as e:
        print(f"Erro de requisição ao chamar LLM API: {e}")
        return "Erro de conexão ao tentar comunicar com o modelo."
    except Exception as e: # Captura outras exceções inesperadas
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
