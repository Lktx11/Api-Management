from flask import g, jsonify, request
import jwt
import time
import sqlite3
import bcrypt
from utils.logger import loggerInfo
from middlewares.middlewares import error as Error
from models.usuarios.usuarios import conectar
cursor = conectar.cursor()


class Auth:
    def registrar(dados):
            if not dados:
                return Error(("Json nao enviado!"), 400)
            if "cpf" not in dados:
                return Error(("Cpf esta faltando!"), 400)
            if "senha" not in dados:
                return Error(("A senha esta faltando!"), 400)
            if dados['senha'] == "" or dados['cpf'] == "":
                return Error(("Cpf ou senha não podem ser vazios!"), 400)
            try:
                senha = dados['senha']  
                senha_bytes = senha.encode("utf-8")
                senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
                senha_db = senha_hash.decode("utf-8")
                cursor.execute("INSERT INTO usuarios (cpf, senha, window, rate_limit) VALUES (?, ?, ?, ?)", (dados['cpf'], senha_db, 60, 10))
                conectar.commit()
                loggerInfo(f"Usuario registrado com sucesso, cpf: {dados['cpf']}")
                return jsonify({
                    "status" : "sucesso",
                    "mensagem" : "Usuario criado com sucesso!"
                }), 201
            except sqlite3.IntegrityError:
                return Error(("Cpf ja registrado!"), 409)
    
    def gerarToken(cpf):
        agora = time.time()
        payload = {
            "cpf" : cpf,
            "exp" : agora + 3600
        }
        token = jwt.encode(payload, "Chave secreta", algorithm="HS256")
        return token
    
    def login(dados):
        cursor.execute("SELECT senha FROM usuarios WHERE cpf = ?", (dados['cpf'],))
        fetch_senha_usuario = cursor.fetchone()
        if fetch_senha_usuario == None:
            return Error(("Usuario não encontrado!"), 404)
        senha_bytes = dados['senha'].encode("utf-8")
        if bcrypt.checkpw(senha_bytes,fetch_senha_usuario[0].encode('utf-8')) == False:
            return Error(("Senha incorreta!"), 401)
        g.cpf = dados['cpf']
        token = Auth.gerarToken(dados['cpf'])
        loggerInfo(f"Usuario logou com sucesso, cpf: {dados['cpf']}")
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Logado com sucesso!",
            "token" : token
        }), 200