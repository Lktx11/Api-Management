from flask import jsonify, request,g
from models.clientes.clientes import conectar
from models.usuarios.usuarios import conectar as conectar_usuarios
from utils.logger import loggerWarning
from functools import wraps
from utils.logger import loggerWarning
import time
import json
import jwt
cursor = conectar.cursor()
cursor_usuarios = conectar_usuarios.cursor()

def error(mensagem, codigo):
    return jsonify({
        "status" : "erro",
        "mensagem" : mensagem
    }), codigo
    
    

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header == None:
            loggerWarning("Nao enviou um token")
            return error(("Token não enviado!"), 400)
        token = auth_header.replace("Bearer ", "")
        try:
            payload = jwt.decode(token, "Chave secreta", algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            loggerWarning("Enviou um token expirado!")
            return error(("Token expirado!"), 401)
        except jwt.InvalidTokenError:
            loggerWarning("Enviou um token invalido!")
            return error(("Token invalido!"), 401)       
        cpf = payload['cpf']
        g.cpf = cpf
        loggerWarning(f"CPF={cpf} | Enviou um token valido! ")
        return func(*args,**kwargs)
    
    return wrapper


def api_key_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if key == None:
            loggerWarning("Nao enviou uma key")
            return error(("Api key não enviada!"), 401)
        cursor.execute("SELECT active, user_cpf FROM clientes WHERE key = ?", (key, ))
        key_dados = cursor.fetchone()
        cpf = key_dados[1]
        g.cpf = cpf
        if key_dados is None:
            loggerWarning(f"Cpf={cpf} | Enviou uma key invalida")  
            return error(("Api key invalida!"), 401 )
        if key_dados[0] == False:
            loggerWarning(f"Cpf={cpf} | Enviou uma key desativada")
            return error(("Key desativada!"), 403)
        loggerWarning(f"Cpf={cpf} | Key={key} | Enviou uma key valida! ")
        g.key = key
        return func(*args, **kwargs)
    return wrapper         

rate = {}

def rate_limit_api(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            agora = time.time()
            metodo_chamado = request.method
            rota_chamada = request.path
            api_key = request.headers.get("X-API-KEY")
            cursor_usuarios.execute("SELECT window, rate_limit, allowed_routes FROM usuarios WHERE cpf = ?", (g.cpf, ))
            usuario_dados = cursor_usuarios.fetchone()
            window = usuario_dados[0]
            rate_limit = usuario_dados[1]
            g.allowed_routes = usuario_dados[2]
            taxa = rate_limit/window

            if api_key not in rate:
                rate[api_key] = {}
            if rota_chamada not in rate[api_key]:
                rate[api_key][rota_chamada] = {}
            if metodo_chamado not in rate[api_key][rota_chamada]:
                rate[api_key][rota_chamada][metodo_chamado] = {
                    "tokens" : rate_limit,
                    "ultimo_update" : agora
                }

            bucket = rate[api_key][rota_chamada][metodo_chamado]
            tempo_passado = agora - bucket['ultimo_update']
            bucket["tokens"] += tempo_passado* taxa
            if bucket["tokens"] > rate_limit:
                bucket["tokens"] = rate_limit 
            if bucket["tokens"] < 1:
                loggerWarning(f"Key={api_key} Utilizou o maximo de request permitidos")
                return error(("Maximo de request atingidos, aguarde!"), 429)            
            bucket["tokens"] -= 1
            bucket["ultimo_update"] = agora
            return func(*args,**kwargs)
        return wrapper


def permission_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        allowed_routes =g.allowed_routes
        if allowed_routes == None:
            return error(("Voce nao tem nenhuma permissao"), 403)
        allowed_routes_json = json.loads(allowed_routes)
        rota_chamada = request.path
        metodo_chamado = request.method.upper()
        permitido = False
        for rota, metodos in allowed_routes_json.items():
            if rota_chamada == rota or rota_chamada.startswith(rota + "/"):
                if metodo_chamado in metodos:
                    permitido = True
                    break

        if not permitido:
            loggerWarning(f"Key={g.key} | Tentou acessar uma rota que nao possui permissao ")
            return error((f"Sem permissao a esta rota"), 403 )
        
        return func(*args, **kwargs)


    return wrapper