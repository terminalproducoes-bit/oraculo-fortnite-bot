import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import time

# --- Configuração do Cache Simples ---
_cache = {}
CACHE_TTL = {"loja": 900, "desafios": 3600}  # TTL em segundos

def get_from_cache(key):
    if key in _cache and (time.time() - _cache[key]['timestamp']) < CACHE_TTL.get(key, 300):
        print(f"HIT no cache para '{key}'")
        return _cache[key]['data']
    print(f"MISS no cache para '{key}'")
    return None

def set_to_cache(key, data):
    _cache[key] = {'timestamp': time.time(), 'data': data}

# --- Módulos de Inteligência ---
def buscar_loja_de_itens():
    cached_data = get_from_cache("loja")
    if cached_data:
        return cached_data

    resposta_formatada = "Visão da Loja: Skin 'Aura' (1500 V-Bucks), Gesto 'Dança' (500 V-Bucks)."
    set_to_cache("loja", resposta_formatada)
    return resposta_formatada

def buscar_desafios_semanais():
    cached_data = get_from_cache("desafios")
    if cached_data:
        return cached_data

    resposta_formatada = "Caminho do Sábio: Desafio 1 (Cause 500 de dano com Rifles), Desafio 2 (Visite Fontes Fumegantes)."
    set_to_cache("desafios", resposta_formatada)
    return resposta_formatada

# --- Servidor Flask ---
app = Flask(__name__)

# ROTA PRINCIPAL (evita erro 404 no Render)
@app.route("/", methods=["GET"])
def home():
    return "Oráculo Fortnite ONLINE ✔️", 200

@app.route("/whatsapp", methods=['GET', 'POST'])
def webhook_whatsapp():

    # GET = Twilio testando / navegador abrindo
    if request.method == 'GET':
        return "OK", 200

    # POST = Mensagem do usuário
    mensagem_usuario = request.values.get('Body', '').lower().strip()
    resp = MessagingResponse()

    if 'loja' in mensagem_usuario:
        corpo_resposta = buscar_loja_de_itens()
    elif 'desafio' in mensagem_usuario:
        corpo_resposta = buscar_desafios_semanais()
    else:
        corpo_resposta = (
            "Saudações, guerreiro. As visões do Oráculo estão ao seu alcance.\n\n"
            "Responda com um dos termos abaixo:\n"
            "➡️ loja — Para ver os tesouros de hoje.\n"
            "➡️ desafios — Para trilhar o caminho da sabedoria."
        )

    resp.message(corpo_resposta)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
