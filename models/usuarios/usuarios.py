import sqlite3
# import json

conectar = sqlite3.connect("./models/usuarios/usuarios.db", check_same_thread=False)
cursor = conectar.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios( 
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               cpf TEXT UNIQUE NOT NULL,
               senha TEXT NOT NULL,
               window INTEGER NOT NULL,
               rate_limit INTEGER NOT NULL,
               allowed_routes TEXT )""")
# cursor.execute("""UPDATE usuarios SET allowed_routes = ? WHERE cpf = ?""", (json.dumps({"/teste": ["POST"]}), "123"))

conectar.commit()