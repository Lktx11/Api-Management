import secrets
from flask import jsonify,g
from models.clientes.clientes import conectar
from utils.logger import loggerInfo
import time
import json
agora = time.time()
cursor = conectar.cursor()
class Clientes:
    def gerarApiKey():
        key = secrets.token_hex(32)
        cpf = g.cpf
        cursor.execute("INSERT INTO clientes (user_cpf, key, active, created_at) VALUES (?,?,?,?)", (cpf, key, True, agora))
        conectar.commit()
        loggerInfo(f"CPF={cpf} | Gerou uma nova API Key")
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Api Key gerada com sucesso!",
            "key" : key
        }), 201
        
    def verKeysAtivas():
        lista_keys = {}
        cursor.execute("SELECT key, created_at FROM clientes WHERE active = ? AND user_cpf = ?", (True, g.cpf))
        keys_ativas = cursor.fetchall()
        for key, created_at in keys_ativas:
            lista_keys[key] = created_at
        loggerInfo(f"CPF={g.cpf} | Listou suas API Keys ativas")
        return jsonify({
            "status" : "sucesso",
            "keys" : lista_keys
            })
        
        
    def desativarKey(dados):
        cpf = g.cpf
        if not dados:
            return jsonify({
                "status" : "erro",
                "mensagem" : "Json nao enviado!"
            }), 400
        if "key" not in dados:
            return jsonify({
                "status" : "erro",
                "mensagem" : "A key esta faltando!"
            }), 400
        cursor.execute("SELECT key FROM clientes WHERE user_cpf = ?",(cpf, ))
        keys_usuario = cursor.fetchall()
        if dados['key'] not in [key[0] for key in keys_usuario]:
            return jsonify({
                "status" : "erro",
                "mensagem" : "Key não encontrada!"
            }), 404
        cursor.execute("UPDATE clientes SET active = ? WHERE key = ?", (False, dados['key']))
        conectar.commit()
        loggerInfo(f"CPF={cpf} | Desativou uma API Key({dados['key']})")
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Key desativada com sucesso!"
        })