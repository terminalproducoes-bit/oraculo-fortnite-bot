import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import traceback

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def webhook_whatsapp():
    resp = MessagingResponse()
    try:
        incoming_msg = request.values.get('Body', '').lower().strip()
        msg = resp.message()

        if 'loja' in incoming_msg:
            msg.body("Oráculo Fortnite: Visão da Loja recebida.")
        elif 'desafio' in incoming_msg:
            msg.body("Oráculo Fortnite: Caminho do Sábio revelado.")
        else:
            msg.body("Oráculo Fortnite: Comando não compreendido. Tente 'loja' ou 'desafio'.")

    except Exception as e:
        error_message = f"Visão Turva! Erro: {traceback.format_exc()}"
        resp_error = MessagingResponse()
        resp_error.message(error_message[:1500])
        return str(resp_error)

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
