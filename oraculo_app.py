import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator # Importamos o validador
import traceback

app = Flask(__name__)

# --- Validador da Twilio ---
# No futuro, usaremos isso para segurança. Por agora, vamos apenas instanciar.
validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN', ''))

@app.route("/whatsapp", methods=['POST'])
def webhook_whatsapp():
    # --- Verificação de Segurança (DESATIVADA PARA TESTE) ---
    # is_valid_request = validator.validate(
    #     request.url,
    #     request.form,
    *   # request.headers.get('X-Twilio-Signature', '')
    # )
    # if not is_valid_request:
    #     return "Falha na validação", 403

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
