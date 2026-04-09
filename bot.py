import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

TOKEN = "8670366173:AAGi2YWANKzKOplC8iislU7x7gTN1i4ph5s"
ADMIN_ID = 5198093605

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

# 📌 ГЛАВНОЕ МЕНЮ
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📱 Продакшн", callback_data="prod"),
            InlineKeyboardButton(text="🎬 Съемка", callback_data="shoot")
        ],
        [
            InlineKeyboardButton(text="🎨 Дизайн", callback_data="design"),
            InlineKeyboardButton(text="🎓 Обучение", callback_data="edu")
        ],
        [
            InlineKeyboardButton(text="💬 Консультация", callback_data="consult")
        ]
    ])

# 📌 НАВИГАЦИЯ
def nav_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="back_main"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_main")
        ]
    ])

# 🚀 СТАРТ
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Добро пожаловать в чат-бот *909.Production*\n\n"
        "*[ Мы создаём, вы побеждаете — продакшн с результатом. ]*\n\n"
        "Этот бот создан, чтобы мы быстро поняли вашу задачу, бюджет и сроки — без лишней переписки.\n\n"
        "Ответьте на несколько вопросов, и мы предложим оптимальное решение под ваш запрос 🚀",
        parse_mode="Markdown"
    )

    await message.answer("👇 Выбери категорию:", reply_markup=main_menu())

# 🎯 CALLBACK
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    data = user_data[user_id]

    # 🏠 главное меню
    if callback.data == "back_main":
        user_data[user_id] = {}
        await callback.message.edit_text("👇 Выбери категорию:", reply_markup=main_menu())
        return

    # 📂 категории
    if callback.data == "prod":
        data["service"] = "Продакшн"
        await callback.message.edit_text(
            "Ты выбрал: Продакшн 📱\n\n"
            "Опиши задачу максимально подробно:\n"
            "— что нужно сделать\n"
            "— для какого проекта\n"
            "— какой результат хочешь получить\n\n"
            "Чем точнее — тем сильнее решение 🚀",
            reply_markup=nav_buttons()
        )

    elif callback.data == "shoot":
        data["service"] = "Съемка"
        await callback.message.edit_text(
            "Ты выбрал: Съемка 🎬\n\n"
            "Опиши задачу максимально подробно:\n"
            "— что нужно снять\n"
            "— формат\n"
            "— цель\n\n"
            "Чем точнее — тем сильнее решение 🚀",
            reply_markup=nav_buttons()
        )

    elif callback.data == "design":
        data["service"] = "Дизайн"
        await callback.message.edit_text(
            "Ты выбрал: Дизайн 🎨\n\n"
            "Опиши задачу:\n"
            "— что нужно создать\n"
            "— стиль / примеры\n"
            "— где будет использоваться\n\n"
            "Сделаем сильный визуал под задачу 🚀",
            reply_markup=nav_buttons()
        )

    elif callback.data == "edu":
        data["service"] = "Обучение"
        await callback.message.edit_text(
            "Ты выбрал: Обучение 🎓\n\n"
            "Напиши:\n"
            "— чему хочешь научиться\n"
            "— текущий уровень\n\n"
            "Подберем формат под тебя 🚀",
            reply_markup=nav_buttons()
        )

    elif callback.data == "consult":
        await callback.message.edit_text(
            "Выбери формат консультации 👇",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Бесплатная", callback_data="free_consult")],
                [InlineKeyboardButton(text="Платная (до 2 часов)", callback_data="paid_consult")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_main")]
            ])
        )

    elif callback.data == "free_consult":
        data["service"] = "Бесплатная консультация"
        await callback.message.edit_text(
            "Бесплатная консультация 💬\n\n"
            "Опиши свою задачу — дадим быстрый разбор",
            reply_markup=nav_buttons()
        )

    elif callback.data == "paid_consult":
        data["service"] = "Платная консультация (до 2 часов)"
        await callback.message.edit_text(
            "Платная консультация 💼\n\n"
            "Разберем задачу глубоко и подготовим стратегию.\n\n"
            "Опиши задачу 👇",
            reply_markup=nav_buttons()
        )

    await callback.answer()

# 🧠 ТЕКСТ
@dp.message()
async def handle(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    data = user_data[user_id]

    # 📌 задача
    if "task" not in data:
        data["task"] = message.text
        await message.answer(
            "💰 Чтобы предложить лучшее решение, напиши бюджет:\n\n"
            "Мы подстраиваемся под задачи — можно сделать как минимально, так и максимально мощно."
        )
        return

    # 📌 бюджет
    if "budget" not in data:
        data["budget"] = message.text
        await message.answer("⏳ Когда планируешь запуск?")
        return

    # 📌 сроки
    if "deadline" not in data:
        data["deadline"] = message.text
        await message.answer(
            "📩 Оставь удобный контакт (Telegram / WhatsApp)\n\n"
            "Свяжемся и предложим решение под твою задачу"
        )
        return

    # 📌 контакт
    if "contact" not in data:
        data["contact"] = message.text

        text = (
            f"🔥 Новая заявка\n\n"
            f"Услуга: {data.get('service','-')}\n"
            f"Задача: {data['task']}\n"
            f"Бюджет: {data['budget']}\n"
            f"Сроки: {data['deadline']}\n"
            f"Контакт: {data['contact']}"
        )

        await bot.send_message(ADMIN_ID, text)

        await message.answer(
            "🔥 Заявка принята\n\n"
            "Мы уже анализируем твою задачу и готовим решение.\n\n"
            "Свяжемся с тобой в течение 1–3 часов."
        )

        await message.answer(
            "📌 Пока мы готовим решение — посмотри наши работы:\n"
            "👉 https://instagram.com/909.production_am"
        )

        user_data[user_id] = {}