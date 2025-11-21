import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import traceback # Essencial para a nossa depuração

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def webhook_whatsapp():
    resp = MessagingResponse()
    try:
        # Lógica principal dentro do bloco 'try'
        incoming_msg = request.values.get('Body', '').lower().strip()
        from_number = request.values.get('From', '')
        
        print(f"Mensagem recebida de {from_number}: {incoming_msg}")

        msg = resp.message()

        if 'loja' in incoming_msg:
            msg.body("Oráculo Fortnite: Visão da Loja recebida.")
        elif 'desafio' in incoming_msg:
            msg.body("Oráculo Fortnite: Caminho do Sábio revelado.")
        else:
            msg.body("Oráculo Fortnite: Comando não compreendido. Tente 'loja' ou 'desafio'.")

        print(f"Resposta preparada: {msg.body}")

    except Exception as e:
        # Se qualquer erro ocorrer, ele será capturado aqui.
        # O Oráculo nos enviará o erro pelo WhatsApp.
        error_message = f"Visão Turva! O Oráculo encontrou um erro no servidor: {traceback.format_exc()}"
        
        # Criamos uma nova resposta de erro
        resp_error = MessagingResponse()
        resp_error.message(error_message[:1500]) # Limita o tamanho da mensagem
        
        print(f"ERRO CAPTURADO: {error_message}")
        return str(resp_error)

    return str(resp)

if __name__ == "__main__":
    # Configuração para rodar no Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
