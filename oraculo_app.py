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
        
        # Lógica principal
        if 'loja' in incoming_msg:
            corpo_resposta = "Oráculo Fortnite: Visão da Loja recebida."
            resp.message(corpo_resposta)
        elif 'desafio' in incoming_msg:
            corpo_resposta = "Oráculo Fortnite: Caminho do Sábio revelado."
            resp.message(corpo_resposta)
        else:
            # Se não for um comando conhecido, respondemos com o texto do template pré-aprovado.
            # A Twilio deve reconhecer e entregar esta mensagem.
            corpo_resposta = "Your appointment is coming up on August 22 at 3:45PM. If you need to change it, please reply back and let us know."
            resp.message(corpo_resposta)

    except Exception as e:
        error_message = f"Visão Turva! Erro: {traceback.format_exc()}"
        resp_error = MessagingResponse()
        resp_error.message(error_message[:1500])
        return str(resp_error)

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
