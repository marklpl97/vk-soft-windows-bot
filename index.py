import os
from flask import Flask, request

app = Flask(__name__)

CONFIRMATION_CODE = os.environ.get("VK_CONFIRMATION_CODE")

@app.route("/", methods=["POST"])
def handle_webhook():
    data = request.json
    if data.get("type") == "confirmation":
        # Возвращаем код из переменной окружения
        return CONFIRMATION_CODE
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
