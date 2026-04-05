import logging
from flask import request, g
import time
start_time = time.time()
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format=("%(asctime)s - %(levelname)s - %(message)s")
)

def loggerWarning(mensagem):
    ip = request.remote_addr
    rota = request.path
    metodo = request.method
    logging.warning(f"Ip={ip} | Rota={rota} | Metodo = {metodo} | {mensagem}")

def loggerInfo(mensagem):
    ip = request.remote_addr
    rota = request.path
    metodo = request.method
    tempo_resposta = time.time() - start_time
    logging.info(f"Ip={ip} | Rota={rota} | Metodo = {metodo} | Tempo de resposta = {tempo_resposta:.2f}s | {mensagem}")