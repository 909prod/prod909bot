import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# 🔑 ВСТАВЬ СЮДА ТОКЕН ИЗ BotFather
TOKEN = "8670366173:AAGi2YWANKzKOplC8iislU7x7gTN1i4ph5s"

# 🧑‍💻 ВСТАВЬ СЮДА СВОЙ TELEGRAM ID
ADMIN_ID = 5198093605

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

# 📌 Кнопки выбора услуги
service_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="SMM"), KeyboardButton(text="Видеосъемка")],
        [KeyboardButton(text="Монтаж"), KeyboardButton(text="Реклама")],
        [KeyboardButton(text="Другое")]
    ],
    resize_keyboard=True
)

# 💰 Кнопки бюджета
budget_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="до 100$")],
        [KeyboardButton(text="100–300$")],
        [KeyboardButton(text="300–1000$")],
        [KeyboardButton(text="1000$+")]
    ],
    resize_keyboard=True
)

# ⏳ Кнопки сроков
deadline_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Срочно")],
        [KeyboardButton(text="До недели")],
        [KeyboardButton(text="До месяца")],
        [KeyboardButton(text="Просто узнать")]
    ],
    resize_keyboard=True
)

# 🚀 Старт
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🔥 Добро пожаловать в Kingdawe Production\n\n"
        "Контент, который привлекает и продаёт.\n\n"
        "Выбери услугу:",
        reply_markup=service_kb
    )

# 🧠 Основная логика
@dp.message()
async def handle(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    data = user_data[user_id]

    # 1. Услуга
    if "service" not in data:
        data["service"] = message.text
        await message.answer("Опиши задачу 👇")
        return

    # 2. Задача
    if "task" not in data:
        data["task"] = message.text
        await message.answer("Выбери бюджет:", reply_markup=budget_kb)
        return

    # 3. Бюджет
    if "budget" not in data:
        data["budget"] = message.text
        await message.answer("Сроки:", reply_markup=deadline_kb)
        return

    # 4. Сроки
    if "deadline" not in data:
        data["deadline"] = message.text
        await message.answer("Оставь свой контакт (Telegram / WhatsApp)")
        return

    # 5. Контакт и отправка заявки
    if "contact" not in data:
        data["contact"] = message.text

        text = (
            f"🔥 Новая заявка\n\n"
            f"Услуга: {data['service']}\n"
            f"Задача: {data['task']}\n"
            f"Бюджет: {data['budget']}\n"
            f"Сроки: {data['deadline']}\n"
            f"Контакт: {data['contact']}"
        )

        # 📩 отправка тебе
        await bot.send_message(ADMIN_ID, text)

        await message.answer("🔥 Заявка принята! Ответим в течение 1–3 часов.")

        # 🔄 очищаем данные
        user_data[user_id] = {}

# ▶️ Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())