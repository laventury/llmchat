# main.py
import os
import sys
import asyncio

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from quart import Quart, send_from_directory, current_app
# A importação do db e user_bp será mantida caso o usuário queira reativar
# a funcionalidade de banco de dados e autenticação de usuário padrão do template.
# from src.models.user import db # Comentado pois não usaremos DB neste template de chat simples
from src.routes.user import user_bp # Mantido para exemplo, mas não essencial para o chat
from src.routes.chat_bp import chat_bp # Importa o blueprint do chat

app = Quart(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT' # Chave secreta para sessões, etc.

# Registrar o blueprint do chat
app.register_blueprint(chat_bp, url_prefix='/api')

# Registrar o blueprint de usuário (exemplo do template original, pode ser removido se não for usado)
# app.register_blueprint(user_bp, url_prefix='/api/users') # Ajuste o prefixo se necessário

# Configuração do banco de dados (comentada, pois não é o foco do chat LLM simples)
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# async def init_db():
#     async with app.app_context():
#         db.create_all()
# asyncio.create_task(init_db())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
async def serve(path):
    static_folder_path = current_app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return await send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return await send_from_directory(static_folder_path, 'index.html')
        else:
            # Se index.html não existir, pode ser uma SPA que lida com rotas no cliente
            # ou simplesmente um erro se um index.html for esperado.
            # Para um template de chat, provavelmente teremos um index.html.
            return "index.html not found in static folder", 404

if __name__ == '__main__':
    # Para rodar com Quart, geralmente se usa um servidor ASGI como Hypercorn ou Uvicorn
    # Exemplo: hypercorn main:app --bind 0.0.0.0:5000
    # O app.run() do Quart é principalmente para desenvolvimento.
    # Para produção, use um servidor ASGI.
    print("Para executar em produção, use um servidor ASGI, por exemplo: hypercorn main:app -b 0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False) # use_reloader=False é bom para dev com async

