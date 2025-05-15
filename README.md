# Template de Chat com LLM Assíncrono (Python/Quart)

Este projeto fornece um template básico para um website de chat com um Large Language Model (LLM), utilizando Python com o framework Quart para o backend (garantindo processamento assíncrono) e HTML, CSS e JavaScript para o frontend.

## Funcionalidades

- **Backend Assíncrono:** Construído com Quart para lidar com múltiplas requisições simultaneamente de forma eficiente.
- **Frontend Responsivo:** Interface de chat simples e responsiva, adaptável a diferentes tamanhos de tela.
- **Integração Flexível com LLM:** Projetado para permitir a troca do modelo LLM com modificações mínimas.

## Estrutura do Projeto

```
llm_chat_template/
├── flask_app/            # Nome mantido do template original, mas usa Quart
│   ├── src/
│   │   ├── models/       # (Opcional, não usado no chat simples)
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat_bp.py  # Blueprint para as rotas do chat
│   │   │   └── user_bp.py  # (Exemplo do template, pode ser removido)
│   │   ├── static/
│   │   │   ├── index.html  # Arquivo principal do frontend
│   │   │   ├── style.css   # Estilos do frontend
│   │   │   └── script.js   # Lógica do frontend (JavaScript)
│   │   ├── __init__.py
│   │   └── main.py       # Ponto de entrada da aplicação Quart
│   ├── venv/             # Ambiente virtual Python
│   └── requirements.txt  # Dependências do Python
├── todo.md               # Lista de tarefas do desenvolvimento (para o agente Manus)
└── README.md             # Este arquivo
```

## Configuração e Execução

### Pré-requisitos

- Python 3.8 ou superior
- `pip` para gerenciamento de pacotes Python

### 1. Configurar Ambiente Virtual e Instalar Dependências

Recomenda-se o uso de um ambiente virtual para isolar as dependências do projeto.

```bash
# Navegue até o diretório flask_app
cd llm_chat_template/flask_app

# Crie um ambiente virtual (se ainda não existir)
python -m venv venv

# Ative o ambiente virtual
# No Linux/macOS:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

**Nota:** O arquivo `requirements.txt` será gerado em uma etapa posterior do desenvolvimento. Por enquanto, você precisará instalar `Quart` e `httpx` manualmente se for executar antes da geração do `requirements.txt`:
`pip install Quart httpx`

### 2. Configurar o Modelo LLM

A integração com o LLM é feita no arquivo `src/routes/chat_bp.py`.

Abra o arquivo `llm_chat_template/flask_app/src/routes/chat_bp.py` e localize as seguintes variáveis de configuração:

```python
# Configuração (idealmente viria de um arquivo de configuração ou variáveis de ambiente)
LLM_API_URL = "YOUR_LLM_API_ENDPOINT_HERE"  # Substitua pelo endpoint real da API do LLM
LLM_API_KEY = "YOUR_LLM_API_KEY_HERE"      # Substitua pela sua chave de API, se necessário
```

- **`LLM_API_URL`**: Substitua `"YOUR_LLM_API_ENDPOINT_HERE"` pelo URL do endpoint da API do LLM que você deseja usar (ex: Gemini, OpenAI, etc.).
- **`LLM_API_KEY`**: Substitua `"YOUR_LLM_API_KEY_HERE"` pela sua chave de API, se o LLM exigir autenticação baseada em chave.

Dentro da função `get_llm_response`, você também precisará adaptar o `payload` para corresponder ao formato esperado pela API do seu LLM específico. O exemplo atual é uma estrutura genérica que inclui um campo `model` e `contents` (similar ao Gemini API):

```python
    payload = {
        "model": "gemini-2.0-flash", # Exemplo, pode ser configurável
        "contents": [{
            "parts": [{
                "text": user_message
            }]
        }]
        # Adapte o payload conforme a API do seu LLM (Gemini, OpenAI, etc.)
    }
```

E a extração da resposta:

```python
            # Extraia a resposta do LLM da estrutura de dados retornada pela API
            # Isto é um exemplo e precisará ser ajustado para a API específica do Gemini 2.0 Flash
            if llm_data.get("candidates") and llm_data["candidates"][0].get("content"): 
                return llm_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                # Fallback ou log de erro se a estrutura da resposta não for a esperada
                print(f"Resposta inesperada do LLM: {llm_data}")
                return "Desculpe, não consegui processar a resposta do modelo no momento."
```

**Para usar o Gemini 2.0 Flash (ou outro modelo Gemini):**
1. Certifique-se de que `LLM_API_URL` aponta para o endpoint correto da API Gemini (ex: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent`).
2. Obtenha uma API Key do Google AI Studio.
3. Atualize `LLM_API_KEY` com sua chave.
4. O payload e a extração da resposta no código atual são um bom ponto de partida para a API Gemini, mas verifique a documentação oficial para garantir compatibilidade total com a versão específica do modelo e da API que você está usando.

**Para usar um modelo da OpenAI (ex: GPT-4):**
1. `LLM_API_URL` seria algo como `https://api.openai.com/v1/chat/completions`.
2. `LLM_API_KEY` seria sua chave da API OpenAI.
3. O `payload` precisaria ser ajustado para o formato da OpenAI, por exemplo:
   ```python
   payload = {
       "model": "gpt-4",
       "messages": [
           {"role": "user", "content": user_message}
       ]
   }
   ```
4. A extração da resposta também mudaria, por exemplo:
   ```python
   return llm_data["choices"][0]["message"]["content"]
   ```

**Recomendação:** Para maior flexibilidade e segurança, considere mover `LLM_API_URL` e `LLM_API_KEY` para variáveis de ambiente em um ambiente de produção.

### 3. Executar a Aplicação

Após configurar o ambiente e as dependências, você pode executar a aplicação Quart.

No diretório `llm_chat_template/flask_app/src` (onde `main.py` está localizado):

```bash
# (Certifique-se de que o ambiente virtual está ativado)
# cd src # se você estiver em flask_app

# Para desenvolvimento:
python main.py
```

Isso iniciará o servidor de desenvolvimento do Quart, geralmente em `http://0.0.0.0:5000/` ou `http://127.0.0.1:5000/`.

Para produção, é recomendado usar um servidor ASGI como Hypercorn ou Uvicorn:

```bash
# Exemplo com Hypercorn (instale com: pip install hypercorn)
hypercorn main:app --bind 0.0.0.0:5000

# Exemplo com Uvicorn (instale com: pip install uvicorn)
uvicorn main:app --host 0.0.0.0 --port 5000
```

Abra seu navegador e acesse o endereço fornecido para interagir com o chat.

## Como o Processamento Assíncrono é Utilizado

- **Quart:** O framework Quart é uma reimplementação assíncrona do Flask, permitindo que as rotas sejam definidas com `async def`.
- **`httpx`:** A biblioteca `httpx` é usada para fazer chamadas HTTP assíncronas para a API do LLM. Isso evita que o servidor bloqueie enquanto espera pela resposta do LLM, permitindo que ele processe outras requisições.
- **`asyncio`:** O Quart utiliza o `asyncio` do Python para gerenciar as operações assíncronas.

Isso garante que o servidor possa lidar com múltiplos usuários interagindo com o chat simultaneamente sem que um usuário esperando pela resposta do LLM afete a responsividade para outros usuários.

## Próximos Passos (Sugestões)

- **Melhorar a Interface do Usuário:** Adicionar mais recursos visuais, indicadores de digitação mais sofisticados, histórico de chat persistente (localStorage ou backend).
- **Gerenciamento de Estado da Conversa:** Implementar um sistema para manter o contexto da conversa com o LLM.
- **Segurança:** Validar entradas, proteger a API Key (usar variáveis de ambiente é um bom começo).
- **Testes:** Escrever testes unitários e de integração.
- **Deployment:** Configurar o deploy para um ambiente de produção (ex: Docker, serviços de nuvem).




## Implantação com Docker

Para facilitar a implantação e garantir um ambiente consistente, um `Dockerfile` é fornecido na raiz do projeto (`llm_chat_template/Dockerfile`).

### Pré-requisitos para Docker

- Docker instalado e em execução na sua máquina.

### Construindo a Imagem Docker

1.  Navegue até o diretório raiz do projeto (`llm_chat_template`), onde o `Dockerfile` está localizado.
2.  Execute o comando a seguir para construir a imagem Docker. Substitua `seu-nome-de-imagem-chat` por um nome de sua escolha para a imagem:

    ```bash
    docker build -t seu-nome-de-imagem-chat .
    ```

    Este comando irá ler o `Dockerfile`, baixar a imagem base do Python, instalar as dependências e copiar os arquivos da sua aplicação para dentro da imagem.

### Executando o Container Docker

Após a imagem ser construída com sucesso, você pode executar um container a partir dela:

```bash
docker run -d -p 5000:5000 --name meu-chat-container seu-nome-de-imagem-chat
```

Explicação dos parâmetros:

-   `-d`: Executa o container em modo "detached" (em segundo plano).
-   `-p 5000:5000`: Mapeia a porta 5000 do seu host para a porta 5000 do container (onde a aplicação Quart/Hypercorn está rodando).
-   `--name meu-chat-container`: Dá um nome ao seu container para facilitar o gerenciamento.
-   `seu-nome-de-imagem-chat`: O nome da imagem que você construiu no passo anterior.

Após executar este comando, a aplicação de chat estará acessível no seu navegador em `http://localhost:5000`.

### Gerenciando o Container

-   **Ver logs do container:**
    ```bash
    docker logs meu-chat-container
    ```

-   **Parar o container:**
    ```bash
    docker stop meu-chat-container
    ```

-   **Iniciar um container parado:**
    ```bash
    docker start meu-chat-container
    ```

-   **Remover o container (após parado):**
    ```bash
    docker rm meu-chat-container
    ```

-   **Listar containers em execução:**
    ```bash
    docker ps
    ```

-   **Listar todos os containers (incluindo parados):**
    ```bash
    docker ps -a
    ```

Com o Docker, você pode facilmente implantar esta aplicação em qualquer ambiente que suporte containers Docker, como serviços de nuvem (AWS ECS, Google Cloud Run, Azure Container Instances) ou em seus próprios servidores.

