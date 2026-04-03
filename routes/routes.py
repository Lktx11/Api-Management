from flask import g, request, jsonify
from app import app
from service.auth import Auth
from service.clientes import Clientes
from middlewares.middlewares import token_required, api_key_required, rate_limit_api

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
def post_criar_key():
    dados = request.get_json()
    request_criar_key = Clientes.gerarApiKey(dados)
    return request_criar_key

@app.route("/key", methods=['GET'])
def get_lista_keys_ativas():
    request_lista_keys = Clientes.verKeysAtivas()
    return request_lista_keys

@app.route('/hello', methods=['GET'])
@api_key_required
def hello_api():
    return jsonify({
        "status": "sucesso",
        "mensagem" : "Api key funfando BOAAAAAAAAA"
    })
#TODO arrumar rate_limit
@app.route("/teste", methods=['GET'])
@api_key_required
@rate_limit_api
def teste():
    return jsonify("teste")
@app.route("/teste", methods=['PUT'])
@api_key_required
@rate_limit_api
def put_teste():
    return jsonify("PUT")
        