import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# === НАСТРОЙКИ (берём из переменных окружения Bothost) ===
VK_TOKEN = os.environ.get("VK_TOKEN")
CONFIRMATION_CODE = os.environ.get("VK_CONFIRMATION_CODE")
CALC_URL = os.environ.get("CALC_URL")
CONTACTS = os.environ.get("CONTACTS")

# === ОБРАБОТКА СООБЩЕНИЙ ===
def send_message(user_id, text, keyboard=None):
    """Отправляет сообщение пользователю"""
    payload = {
        "user_id": user_id,
        "message": text,
        "access_token": VK_TOKEN,
        "v": "5.199",
        "random_id": 0
    }
    if keyboard:
        payload["keyboard"] = keyboard
    requests.post("https://api.vk.com/method/messages.send", data=payload)

@app.route("/", methods=["POST"])
def handle_webhook():
    data = request.json
    # Проверка типа уведомления от ВК
    if data.get("type") == "confirmation":
        # Отвечаем кодом подтверждения
        return CONFIRMATION_CODE
    elif data.get("type") == "message_new":
        message = data["object"]["message"]
        user_id = message["from_id"]
        text = message["text"].lower().strip()

        # Логика ответа
        if text in ["привет", "начать", "start"]:
            keyboard = {
                "buttons": [
                    [{"action": {"type": "text", "label": "📐 Рассчитать стоимость"}, "color": "positive"}],
                    [{"action": {"type": "text", "label": "📅 Записаться на замер"}, "color": "primary"}]
                ]
            }
            send_message(user_id, "Добрый день! 👋\n\nВыберите, что вас интересует:", keyboard=keyboard)
        elif "рассчитать стоимость" in text:
            send_message(user_id, f"📐 Ссылка на калькулятор:\n{CALC_URL}")
        elif "записаться на замер" in text:
            send_message(user_id, f"📞 Наши контакты:\n{CONTACTS}")
        else:
            send_message(user_id, "Напишите 'Привет' или 'Начать'")
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
