from flask import g, request, jsonify
from app import app
from service.auth import Auth
from service.clientes import Clientes
from middlewares.middlewares import token_required, api_key_required, rate_limit_api, permission_required

#usuario
@app.route("/registrar", methods=['POST'])
def post_registrar_usuario():
    dados = request.get_json()
    request_registrar = Auth.registrar(dados)
    return request_registrar

@app.route("/login", methods=['POST'])
def post_login_usuario():
    dados = request.get_json()
    request_login = Auth.login(dados)
    return request_login
#keys
@app.route("/key", methods=['POST'])
@token_required
def post_criar_key():
    dados = request.get_json()
    request_criar_key = Clientes.gerarApiKey(dados)
    return request_criar_key

@app.route("/key", methods=['GET'])
@token_required
def get_lista_keys_ativas():
    request_lista_keys = Clientes.verKeysAtivas()
    return request_lista_keys

#testes

@app.route("/teste", methods=['GET'])
@api_key_required
@rate_limit_api
@permission_required
def teste():
    return jsonify("GET")

@app.route("/teste", methods=['POST'])
@api_key_required
@rate_limit_api
@permission_required
def testepost():
    return jsonify("POST")

        

        