from flask import request, jsonify, Blueprint
from service.auth import Auth
from service.clientes import Clientes
from middlewares.middlewares import token_required, api_key_required, rate_limit_api, permission_required
from flasgger import swag_from
routes_bp = Blueprint('routes', __name__)

#usuario
@routes_bp.route("/registrar", methods=['POST'])
@swag_from("../docs/auths/register.yaml")
def post_registrar_usuario():
   
    dados = request.get_json()
    request_registrar = Auth.registrar(dados)
    return request_registrar

@routes_bp.route("/login", methods=['POST'])
@swag_from("../docs/auths/login.yaml")
def post_login_usuario():
    dados = request.get_json()
    request_login = Auth.login(dados)
    return request_login

#keys
@routes_bp.route("/key/criar", methods=['POST'])
@token_required
@swag_from("../docs/clientes/criarApiKey.yaml")
def post_criar_key():
    request_criar_key = Clientes.gerarApiKey()
    return request_criar_key

@routes_bp.route("/key/lista", methods=['GET'])
@token_required
@swag_from("../docs/clientes/listarKeyAtivas.yaml")
def get_lista_keys_ativas():
    request_lista_keys = Clientes.verKeysAtivas()
    return request_lista_keys

@routes_bp.route("/key/desativar", methods=['POST'])
@token_required
def post_desativar_key():
    dados = request.get_json()
    request_desativar_key = Clientes.desativarKey(dados)
    return request_desativar_key
#testes

@routes_bp.route("/teste", methods=['GET'])
@api_key_required
@rate_limit_api
@permission_required
def teste():
    return jsonify("GET")

@routes_bp.route("/teste", methods=['POST'])
@api_key_required
@rate_limit_api
@permission_required
def testepost():
    return jsonify("POST")
print("Routes carregados!")

        

        