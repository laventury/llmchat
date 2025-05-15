# test_async.py
import asyncio
import httpx
import time

TARGET_URL = "http://127.0.0.1:5000/api/chat"
NUM_REQUESTS = 10  # Número de requisições simultâneas

async def send_request(client, i):
    payload = {"message": f"Olá, esta é a mensagem de teste número {i+1}"}
    print(f"Enviando requisição {i+1}...")
    try:
        start_time = time.time()
        response = await client.post(TARGET_URL, json=payload, timeout=60.0)
        end_time = time.time()
        response_data = response.json()
        print(f"Requisição {i+1} concluída em {end_time - start_time:.2f}s. Status: {response.status_code}. Resposta: {response_data}")
        return response.status_code, response_data
    except httpx.ConnectError as e:
        print(f"Erro de conexão na requisição {i+1}: {e}. Verifique se o servidor está rodando em {TARGET_URL}.")
        return "CONNECT_ERROR", str(e)
    except Exception as e:
        print(f"Erro na requisição {i+1}: {e}")
        return "ERROR", str(e)

async def main():
    print(f"Iniciando teste com {NUM_REQUESTS} requisições para {TARGET_URL}")
    async with httpx.AsyncClient() as client:
        tasks = [send_request(client, i) for i in range(NUM_REQUESTS)]
        results = await asyncio.gather(*tasks)
    
    print("\n--- Resumo dos Resultados ---")
    success_count = 0
    error_count = 0
    connect_error_count = 0

    for i, (status, data) in enumerate(results):
        if status == "CONNECT_ERROR":
            connect_error_count += 1
            print(f"Resultado {i+1}: Erro de Conexão - {data}")
        elif status == "ERROR" or (isinstance(status, int) and status >= 400):
            error_count += 1
            print(f"Resultado {i+1}: Erro (Status: {status}) - {data}")
        else:
            success_count += 1
            print(f"Resultado {i+1}: Sucesso (Status: {status}) - {data}")
    
    print(f"\nTotal de Sucessos: {success_count}")
    print(f"Total de Erros (aplicação/servidor): {error_count}")
    print(f"Total de Erros de Conexão: {connect_error_count}")

    if connect_error_count > 0:
        print("\nAVISO: Algumas requisições falharam devido a erros de conexão. Verifique se o servidor Quart está em execução e acessível.")
    if error_count > 0 and connect_error_count == 0:
        print("\nAVISO: Algumas requisições resultaram em erro. Como o endpoint do LLM não está configurado, isso é esperado (o servidor deve retornar um erro do LLM). O importante é que as requisições foram processadas.")
    if success_count == NUM_REQUESTS:
        print("\nTodas as requisições foram processadas com sucesso (retornando a resposta esperada do endpoint, mesmo que seja um erro do LLM).")

if __name__ == "__main__":
    asyncio.run(main())

