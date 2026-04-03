import sqlite3

conectar = sqlite3.connect("./models/clientes/clientes.db", check_same_thread=False)
cursor = conectar.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS clientes( 
               app_name TEXT PRIMARY KEY NOT NULL,
               key TEXT UNIQUE NOT NULL,
               active INTEGER NOT NULL 
               )""") #0 - desativado 1 - ativado
conectar.commit()