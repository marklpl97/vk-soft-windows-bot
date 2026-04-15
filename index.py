import asyncio
import os
from dotenv import load_dotenv
import re
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

# Загружаем переменные из .env
load_dotenv()

# Токен
TOKEN = os.getenv("VK_TOKEN")

# Ссылка на калькулятор
CALC_URL = os.getenv("CALC_URL", "https://ссылка_по_умолчанию")  # второй аргумент — значение по умолчанию
CONTACTS = os.getenv("CONTACTS", "📞 Контакты не указаны")


bot = Bot(token=TOKEN)

def get_keyboard():
    keyboard = Keyboard()
    keyboard.add(Text("📐 Рассчитать стоимость"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("📅 Записаться на замер"), color=KeyboardButtonColor.PRIMARY)
    return keyboard

def is_phone_number(text):
    """Проверяет, похоже ли сообщение на номер телефона (10-11 цифр)."""
    # Убираем все нецифровые символы (пробелы, дефисы, скобки, плюс)
    digits = re.sub(r'\D', '', text)
    # Если осталось 10 или 11 цифр — считаем номером телефона
    return len(digits) in [10, 11]

@bot.on.message()
async def handle_message(message: Message):
    text = message.text.lower()
    original_text = message.text  # сохраняем исходный текст для проверки номера
    
    # Проверяем, не отправил ли пользователь номер телефона
    if is_phone_number(original_text):
        await message.answer(
            "✅ Мы перезвоним Вам в ближайшее время.\n"
            "Спасибо, что обратились к нам! 🌿"
        )
        return
    
    # Обычные команды
    if text in ["привет", "начать", "start"]:
        await message.answer(
            "Добрый день! 👋\n\n"
            "Я бот компании Территория комфорта. Мы производим для вас мягкие окна.\n"
            "Выберите, что вас интересует: Рассчитать стоимость или Записаться на замер",
            keyboard=get_keyboard()
        )
    
    elif "рассчитать стоимость" in text:
        await message.answer(
            f"📐 Для расчёта стоимости мягких окон перейдите по ссылке:\n{CALC_URL}\n\n"
            "Выберите город, плёнку, количество окон, крепёж и введите размеры."
        )
    
    elif "записаться на замер" in text:
        await message.answer(
            f"📞 Для записи на замер свяжитесь с нами:\n\n{CONTACTS}\n\n"
            "Или напишите номер телефона и мы перезвоним вам в ближайшее время."
        )
    
    else:
        await message.answer(
            "Извините, я не понимаю эту команду.\n"
            "Напишите 'Привет' или 'Начать', чтобы увидеть меню.\n\n"
        )

if __name__ == "__main__":
    print("Бот запущен...")
    try:
        bot.run_forever()
    except Exception as e:
        print(f"Ошибка: {e}")