import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command

TOKEN = "тут будет токен"
ADMIN_ID = 5198093605

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

# 📌 КАТЕГОРИИ
category_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Продакшн"), KeyboardButton(text="🎬 Съемка")],
        [KeyboardButton(text="🎨 Дизайн"), KeyboardButton(text="🎓 Обучение")],
        [KeyboardButton(text="💬 Консультация")]
    ],
    resize_keyboard=True
)

# 📌 ПРОДАКШН
production_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="SMM"), KeyboardButton(text="Упаковка профиля")],
        [KeyboardButton(text="Написание сценариев")]
    ],
    resize_keyboard=True
)

# 📌 СЪЕМКА
shoot_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Видеосъемка"), KeyboardButton(text="Фотосессия")],
        [KeyboardButton(text="Съемка на дрон"), KeyboardButton(text="Репортажная съемка")]
    ],
    resize_keyboard=True
)

# 📌 ДИЗАЙН
design_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Digital дизайн"), KeyboardButton(text="Print дизайн")]
    ],
    resize_keyboard=True
)

# 📌 ОБУЧЕНИЕ
education_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Обучение монтажу"), KeyboardButton(text="Обучение съемке")],
        [KeyboardButton(text="Обучение сценариям"), KeyboardButton(text="Поведение в кадре")]
    ],
    resize_keyboard=True
)

# 📌 КОНСУЛЬТАЦИЯ
consult_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Бесплатная консультация")],
        [KeyboardButton(text="Платная консультация (до 2 часов)")]
    ],
    resize_keyboard=True
)

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

    await message.answer("👇 Выбери категорию:", reply_markup=category_kb)

# 🧠 ЛОГИКА
@dp.message()
async def handle(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    data = user_data[user_id]

    # 📂 категории
    if message.text == "📱 Продакшн":
        await message.answer("Выбери услугу 👇", reply_markup=production_kb)
        return

    if message.text == "🎬 Съемка":
        await message.answer("Выбери услугу 👇", reply_markup=shoot_kb)
        return

    if message.text == "🎨 Дизайн":
        await message.answer("Выбери услугу 👇", reply_markup=design_kb)
        return

    if message.text == "🎓 Обучение":
        await message.answer("Выбери услугу 👇", reply_markup=education_kb)
        return

    if message.text == "💬 Консультация":
        await message.answer(
            "Выбери формат консультации 👇\n\n"
            "🔹 Бесплатная — быстрый разбор\n"
            "🔹 Платная (до 2 часов) — глубокая проработка стратегии",
            reply_markup=consult_kb
        )
        return

    # 📌 консультации
    if message.text == "Бесплатная консультация":
        data["service"] = "Бесплатная консультация"
        await message.answer("Опиши свою задачу 👇", reply_markup=ReplyKeyboardRemove())
        return

    if message.text == "Платная консультация (до 2 часов)":
        data["service"] = "Платная консультация (до 2 часов)"
        await message.answer(
            "Отлично 👌\n\n"
            "Опиши задачу — мы подготовим стратегию и разберем её на созвоне",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    # 📌 услуга
    if "service" not in data:
        data["service"] = message.text
        await message.answer(
            "Отлично 👌\n\n"
            "Опиши задачу максимально подробно:\n"
            "— что нужно сделать\n"
            "— для какого проекта\n"
            "— какой результат хочешь получить",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    # 📌 задача
    if "task" not in data:
        data["task"] = message.text
        await message.answer(
            "💰 Чтобы предложить лучшее решение — выбери бюджет:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="до 100$")],
                    [KeyboardButton(text="100–300$")],
                    [KeyboardButton(text="300–1000$")],
                    [KeyboardButton(text="1000$+")]
                ],
                resize_keyboard=True
            )
        )
        return

    # 📌 бюджет
    if "budget" not in data:
        data["budget"] = message.text
        await message.answer(
            "⏳ Когда планируешь запуск?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Срочно")],
                    [KeyboardButton(text="До недели")],
                    [KeyboardButton(text="До месяца")],
                    [KeyboardButton(text="Просто узнать")]
                ],
                resize_keyboard=True
            )
        )
        return

    # 📌 сроки
    if "deadline" not in data:
        data["deadline"] = message.text
        await message.answer(
            "📩 Оставь удобный контакт (Telegram / WhatsApp)",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    # 📌 контакт
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

        await bot.send_message(ADMIN_ID, text)

        await message.answer(
            "🔥 Заявка принята\n\n"
            "Мы уже анализируем твой запрос.\n"
            "Свяжемся с тобой в течение 1–3 часов."
        )

        await message.answer(
            "📌 Пока мы готовим решение — посмотри наши работы:\n"
            "👉 https://instagram.com/909.production_am"
        )

        user_data[user_id] = {}

# ▶️ запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())