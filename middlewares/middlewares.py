from flask import jsonify, request,g
from models.clientes.clientes import conectar
from functools import wraps
import time
import json
import logging
import jwt
cursor = conectar.cursor()
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format=("%(asctime)s - %(levelname)s - %(message)s")
)

def loggerWarning(mensagem):
    ip = request.remote_addr
    rota = request.path
    metodo = request.method
    logging.warning(f"Ip={ip} | Rota={rota} | Metodo = {metodo} | {mensagem}")

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
        cursor.execute("SELECT active, rate_limit, window, allowed_routes FROM clientes WHERE key = ?", (key, ))
        key_dados = cursor.fetchone()
        if key_dados is None:
            loggerWarning("Nao enviou uma key valida")
            return error(("Api key invalida!"), 401 )
        if key_dados[0] == 0:
            loggerWarning("Enviou uma key desativada")
            return error(("Key desativada!"), 403)
        loggerWarning(f"Key={key} | Utilizou sua key")
        g.rate_limit = key_dados[1] or 10
        g.window = key_dados[2] or 60
        g.key = key
        g.allowed_routes = key_dados[3]
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
            window = g.window
            rate_limit = g.rate_limit
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
        allowed_routes = g.allowed_routes
        if allowed_routes == None:
            return error(("Voce nao tem nenhuma permissao"), 403)
        rota_chamada = request.path
        permitido = False
        for rota in allowed_routes:
            if rota_chamada == rota or rota_chamada.startswith(rota + "/"):
                permitido = True
                break

        if not permitido:
            loggerWarning(f"Key={g.key} | Tentou acessar uma rota que nao possui permissao ")
            return error((f"Sem permissao a esta rota"), 403 )
        
        return func(*args, **kwargs)


    return wrapper