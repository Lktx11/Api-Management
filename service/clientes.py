import secrets
from flask import jsonify
from models.clientes.clientes import conectar
cursor = conectar.cursor()
class Clientes:
    def gerarApiKey(dados):
        nome = dados['nome']
        key = secrets.token_hex(32)
        cursor.execute("INSERT INTO clientes (app_name, key, active, rate_limit, window) VALUES (?,?,?,?,?)", (nome, key, 1, 10, 60))
        conectar.commit()
        return jsonify({
            "status" : "sucesso",
            "mensagem" : "Api Key gerada com sucesso!",
            "key" : key
        })
        
    def verKeysAtivas():
        lista_keys = {}
        cursor.execute("SELECT app_name, key FROM clientes WHERE active = ?", (1, ))
        keys_ativas = cursor.fetchall()
        for app, key in keys_ativas:
            lista_keys[app] = key
        return jsonify({
            "status" : "sucesso",
            "keys" : lista_keys
            })
        
        
        