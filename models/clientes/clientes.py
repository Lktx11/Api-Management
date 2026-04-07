import sqlite3

conectar = sqlite3.connect("./models/clientes/clientes.db", check_same_thread=False)
cursor = conectar.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS clientes( 
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_cpf INTEGER NOT NULL,
               key TEXT UNIQUE NOT NULL,
               active boolean NOT NULL,
               created_at INTEGER NOT NULL
               )""") 


conectar.commit()   