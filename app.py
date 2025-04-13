from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "my_ig_bot_token"  # Укажи такой же токен в Meta

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Verification failed", 403

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("🔔 Новое сообщение:", data)
    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
