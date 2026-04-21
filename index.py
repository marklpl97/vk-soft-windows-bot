import os
import re
from pathlib import Path

import vk_api
from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import ApiError
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("VK_TOKEN")
GROUP_ID = os.getenv("VK_GROUP_ID")

if not TOKEN:
    raise ValueError("VK_TOKEN не найден в .env")
if not GROUP_ID:
    raise ValueError("VK_GROUP_ID не найден в .env")

GROUP_ID = int(GROUP_ID)

WELCOME_TEXT = (
    "Добрый день!\n"
    "Я бот компании Территория комфорта. Мы производим мягкие окна.\n"
    "Напишите, что вас интересует: Рассчитать стоимость или Записаться на замер."
)

MEASURE_TEXT = (
    "Позвоните или напишите нам\n"
    "📞 Марина: +7 995 601 7892\n"
    "📞 Max: +7 995 288 4484\n"
    "или оставьте свой номер телефона и мы Вам перезвоним."
)

THANKS_TEXT = "Спасибо, что выбрали нас! Мы Вам перезвоним в ближайшее время."

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

def main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("Рассчитать стоимость", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Записаться на замер", color=VkKeyboardColor.SECONDARY)
    return keyboard

def calc_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_openlink_button("Рассчитать стоимость", "https://marklpl97.github.io/oknavkmob/")
    keyboard.add_line()
    keyboard.add_button("Записаться на замер", color=VkKeyboardColor.SECONDARY)
    return keyboard

def send_message(user_id, message, keyboard=None):
    params = {
        "user_id": user_id,
        "message": message,
        "random_id": get_random_id()
    }
    if keyboard:
        params["keyboard"] = keyboard.get_keyboard()

    try:
        vk.messages.send(**params)
    except ApiError as e:
        if e.code == 901:
            print(f"Пользователь {user_id} запретил сообщения от сообщества")
        else:
            raise

def is_phone(text):
    t = re.sub(r"\s+", "", text)
    return bool(
        re.fullmatch(r"\+7\d{10}", t) or
        re.fullmatch(r"\d{10}", t) or
        re.fullmatch(r"\d{11}", t)
    )

def handle_message(text, user_id):
    low = text.lower().strip()

    if is_phone(text):
        send_message(user_id, THANKS_TEXT, main_keyboard())
        return

    if low == "рассчитать стоимость":
        send_message(user_id, "Нажмите кнопку ниже для расчета стоимости:", calc_keyboard())
        return

    if low == "записаться на замер":
        send_message(user_id, MEASURE_TEXT, main_keyboard())
        return

    send_message(user_id, WELCOME_TEXT, main_keyboard())

def main():
    print("Бот запущен...")
    for event in longpoll.listen():
        if event.type != VkBotEventType.MESSAGE_NEW:
            continue

        msg = event.message
        text = msg.get("text", "").strip()
        user_id = msg.get("from_id")

        if not text or not user_id:
            continue

        handle_message(text, user_id)

if __name__ == "__main__":
    main()
