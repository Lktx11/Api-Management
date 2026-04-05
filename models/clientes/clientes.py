import sqlite3
# import json

conectar = sqlite3.connect("./models/clientes/clientes.db", check_same_thread=False)
cursor = conectar.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS clientes( 
               app_name TEXT PRIMARY KEY NOT NULL,
               key TEXT UNIQUE NOT NULL,
               active INTEGER NOT NULL 
               )""") #0 - desativado 1 - ativado


# cursor.execute("""UPDATE clientes SET allowed_routes = ? WHERE key = ?""", (json.dumps({"/teste": ["POST"]}), "b0ffd4d7938533eea54477711671185fcfcfb4e1cde4ad80cefc93d6ee8ae400"))
conectar.commit()