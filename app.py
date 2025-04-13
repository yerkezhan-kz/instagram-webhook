from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = "my_ig_bot_token"
PAGE_ACCESS_TOKEN = "ВАШ_ПОЛНЫЙ_PAGE_ACCESS_TOKEN"

# Верификация Webhook
@app.route('/', methods=['GET'])
def verify():
    if (
        request.args.get("hub.mode") == "subscribe"
        and request.args.get("hub.verify_token") == VERIFY_TOKEN
    ):
        return request.args.get("hub.challenge"), 200
    return "Verification failed", 403

# Обработка входящих сообщений
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("🔔 Новое сообщение:", data)

    try:
        for entry in data.get("entry", []):
            messaging = entry.get("messaging", [])
            for message_event in messaging:
                sender_id = message_event["sender"]["id"]

                if "message" in message_event:
                    text = message_event["message"].get("text", "")
                    send_message(sender_id, f"Спасибо за сообщение: '{text}' 👋")

    except Exception as e:
        print("Ошибка обработки:", e)

    return "ok", 200

# Функция отправки ответа
def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v19.0/me/messages"
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    response = requests.post(url, params=params, headers=headers, json=payload)
    print("📨 Ответ отправлен:", response.status_code, response.text)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
