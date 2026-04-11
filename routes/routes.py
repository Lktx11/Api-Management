from flask import request, jsonify, Blueprint
from service.auth import Auth
from service.clientes import Clientes
from middlewares.middlewares import token_required, api_key_required, rate_limit_api, permission_required, rate_limit_login
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
@rate_limit_login
@swag_from("../docs/auths/login.yaml")
def post_login_usuario():
    dados = request.get_json()
    return Auth.login(dados)

#keys
@routes_bp.route("/keys/criar", methods=['POST'])
@token_required
@swag_from("../docs/clientes/criarApiKey.yaml")
def post_criar_key():
    return Clientes.gerarApiKey()

@routes_bp.route("/keys/lista", methods=['GET'])
@token_required
@swag_from("../docs/clientes/listarKeyAtivas.yaml")
def get_lista_keys_ativas():
    return Clientes.verKeysAtivas()

@routes_bp.route("/keys/desativar", methods=['POST'])
@token_required
@swag_from("../docs/clientes/desativarKey.yaml")
def post_desativar_key():
    dados = request.get_json()
    return Clientes.desativarKey(dados)
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

        

        