import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações do webhook
VERIFY_TOKEN = "e0kPl9QgCasVtW9oygSawI7olsH"  # Token de verificação configurado no Facebook
API_HOSTNAME = "https://graph.facebook.com"
API_PATH = "/v21.0/488853444314160/messages"
TOKEN = "YOUR_API_TOKEN_HERE"  # Token de acesso à API do WhatsApp
BOT_NAME = "Amigo Secreto"  # Nome do bot para a mensagem de boas-vindas


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificação do webhook
        params = request.args
        mode = params.get("hub.mode")
        token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                print("WEBHOOK_VERIFIED")
                return challenge, 200
            else:
                return "Forbidden", 403
        return "Not Found", 404

    elif request.method == 'POST':
        # Processa mensagens recebidas
        body = request.json
        print(f"Webhook received: {json.dumps(body)}")

        if body:
            try:
                # Extraindo informações da mensagem
                entry = body.get("entry", [])[0]
                change = entry.get("changes", [])[0]
                value = change.get("value", {})
                contacts = value.get("contacts", [])[0]
                messages = value.get("messages", [])[0]

                username = contacts.get("profile", {}).get("name")
                from_phone = contacts.get("wa_id")
                message_body = messages.get("text", {}).get("body")

                # Montando mensagem de resposta
                response_message = {
                    "messaging_product": "whatsapp",
                    "preview_url": False,
                    "recipient_type": "individual",
                    "to": from_phone,
                    "type": "text",
                    "text": {
                        "body": f"Hi {username}, \n\nMy name is {BOT_NAME}\n\nYour phone number is '{from_phone}' and you wrote me '{message_body}'.\n\nPlease give me a moment to process your request ..."
                    }
                }

                # Enviando resposta via API do WhatsApp
                response = requests.post(
                    f"{API_HOSTNAME}{API_PATH}",
                    headers={
                        "Authorization": f"Bearer {TOKEN}",
                        "Content-Type": "application/json"
                    },
                    data=json.dumps(response_message)
                )

                print(f"WhatsApp API response: {response.json()}")
                return jsonify(response.json()), response.status_code
            except Exception as e:
                print(f"Error processing message: {str(e)}")
                return jsonify({"error": str(e)}), 500
        return "Not Found", 404


if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
