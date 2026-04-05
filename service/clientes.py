import secrets
from flask import jsonify,g
from models.clientes.clientes import conectar
from logger import loggerInfo
import time
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
        })
        
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
        
        
        