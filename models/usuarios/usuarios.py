import sqlite3

conectar = sqlite3.connect("./models/usuarios/usuarios.db", check_same_thread=False)
cursor = conectar.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios( 
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               cpf TEXT UNIQUE NOT NULL,
               senha TEXT NOT NULL)""")

conectar.commit()