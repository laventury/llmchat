# Dockerfile para a aplicação de Chat com Quart

# 1. Usar uma imagem base Python oficial
# Escolha uma versão do Python que seja compatível com suas dependências (ex: 3.11)
FROM python:3.11-slim

# 2. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copiar o arquivo de dependências primeiro para aproveitar o cache do Docker
# Assumindo que o Dockerfile está na raiz do projeto (llm_chat_template) e a app está em flask_app
COPY ./flask_app/requirements.txt .

# 4. Instalar as dependências
# --no-cache-dir para reduzir o tamanho da imagem
# --upgrade pip para garantir a versão mais recente do pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir hypercorn # Adicionar Hypercorn explicitamente se não estiver no requirements.txt

# 5. Copiar o restante dos arquivos da aplicação para o diretório de trabalho
# Copia todo o conteúdo de flask_app para /app no container
COPY ./flask_app/ .

# 6. Expor a porta em que a aplicação Quart (via Hypercorn) estará rodando
# O main.py está configurado para rodar na porta 5000
EXPOSE 5000

# 7. Comando para rodar a aplicação quando o container iniciar
# Usar Hypercorn para rodar a aplicação Quart (ASGI)
# O main.py está em /app/src/main.py
# O objeto da aplicação é 'app'
# Bind para 0.0.0.0 para ser acessível de fora do container
CMD ["hypercorn", "src.main:app", "--bind", "0.0.0.0:5000"]

