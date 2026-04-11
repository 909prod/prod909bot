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
            InlineKeyboardButton(text="📱 Продакшен", callback_data="prod"),
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
        "Добро пожаловать в чат-бот 909.Production\n\n"
        "[ Мы создаём, вы побеждаете - продакшн с результатом. ]\n\n"
        "Этот бот создан, чтобы мы быстро поняли вашу задачу, бюджет и сроки — без лишней переписки.\n\n"
        "Ответьте на несколько вопросов, и мы предложим оптимальное решение под ваш запрос 🚀"
    )

    await message.answer("👇 Выбери направление:", reply_markup=main_menu())

# 🎯 CALLBACK
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    data = user_data[user_id]

    if callback.data == "back_main":
        user_data[user_id] = {}
        await callback.message.edit_text("👇 Выбери направление:", reply_markup=main_menu())
        return

    if callback.data == "prod":
        data["service"] = "Продакшен"
        await callback.message.edit_text(
            "📱 Продакшн\n\n"
            "Опиши задачу максимально подробно:\n"
            "— что нужно сделать\n"
            "— для какого проекта\n"
            "— какой результат хочешь получить\n\n"
            "👉 Чем точнее опишешь — тем сильнее решение предложим",
            reply_markup=nav_buttons()
        )

    elif callback.data == "shoot":
        data["service"] = "Съемка"
        await callback.message.edit_text(
            "🎬 Съемка\n\n"
            "Опиши задачу:\n"
            "— что снимаем\n"
            "— формат (рилс / реклама / YouTube)\n"
            "— цель\n\n"
            "👉 Сделаем не просто видео, а инструмент продаж",
            reply_markup=nav_buttons()
        )

    elif callback.data == "design":
        data["service"] = "Дизайн"
        await callback.message.edit_text(
            "🎨 Дизайн\n\n"
            "Опиши:\n"
            "— что нужно создать\n"
            "— стиль / примеры\n"
            "— где будет использоваться\n\n"
            "👉 Сделаем визуал, который выделит тебя среди конкурентов",
            reply_markup=nav_buttons()
        )

    elif callback.data == "edu":
        data["service"] = "Обучение"
        await callback.message.edit_text(
            "🎓 Обучение\n\n"
            "Напиши:\n"
            "— чему хочешь научиться\n"
            "— текущий уровень\n\n"
            "👉 Подберём формат под тебя, без воды",
            reply_markup=nav_buttons()
        )

    elif callback.data == "consult":
        await callback.message.edit_text(
            "💬 Консультация\n\nВыбери формат 👇",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Бесплатная", callback_data="free_consult")],
                [InlineKeyboardButton(text="Платная (до 2 часов)", callback_data="paid_consult")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_main")]
            ])
        )

    elif callback.data == "free_consult":
        data["service"] = "Бесплатная консультация (15-30 минут)"
        await callback.message.edit_text(
            "💬 Бесплатная консультация\n\n"
            "Опиши задачу — дадим быстрый разбор и направление 👇",
            reply_markup=nav_buttons()
        )

    elif callback.data == "paid_consult":
        data["service"] = "Платная консультация (до 2 часов)"
        await callback.message.edit_text(
            "💼 Платная консультация\n\n"
            "Разберём задачу глубоко и выстроим стратегию.\n\n"
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

    # ✅ если уже завершено
    if data.get("done"):
        await message.answer("❤️ Мы Вам ответим в течение 1–3 часов. Спасибо за ожидание!")
        return

    # ✅ если ждём сообщение после заявки
    if data.get("wait_refs"):
        await message.answer("❤️ Мы Вам ответим в течение 1–3 часов. Спасибо за ожидание!")
        user_data[user_id]["done"] = True
        user_data[user_id].pop("wait_refs", None)
        return

    if "task" not in data:
        data["task"] = message.text
        await message.answer(
            "💰 Напиши примерный бюджет:\n\n"
            "Мы подстраиваемся под задачи — можно сделать как базово, так и на максимальный результат."
        )
        return

    if "budget" not in data:
        data["budget"] = message.text
        await message.answer(
            "⏳ Когда планируешь запуск?\n\n"
            "Это поможет правильно распределить ресурсы под твою задачу"
        )
        return

    if "deadline" not in data:
        data["deadline"] = message.text
        await message.answer(
            "📎 Отправь 1–2 референса одним сообщением 👇\n\n"
            "Это могут быть:\n"
            "— ссылки\n"
            "— скриншоты\n"
            "— видео"
        )
        return

    if "references" not in data:
        data["references"] = message.text
        await message.answer(
            "📩 Оставь контакт (Telegram / WhatsApp)\n\n"
            "Мы свяжемся и предложим решение под твой запрос"
        )
        return

    if "contact" not in data:
        data["contact"] = message.text

        text = (
            f"🔥 Новая заявка\n\n"
            f"Услуга: {data.get('service','-')}\n"
            f"Задача: {data['task']}\n"
            f"Бюджет: {data['budget']}\n"
            f"Сроки: {data['deadline']}\n"
            f"Контакт: {data['contact']}\n"
            f"Референсы: {data.get('references','-')}"
        )

        await bot.send_message(ADMIN_ID, text)

        await message.answer(
            "🔥 Заявка принята\n\n"
            "Мы уже разбираем твою задачу и готовим сильное решение.\n\n"
            "Свяжемся с тобой в течение 1–3 часов."
        )

        await message.answer(
            "📌 Пока мы готовим решение — посмотри наши работы 👇\n"
            "👉 https://instagram.com/909.production_am\n\n"
            "Это даст тебе понимание уровня и подхода 🚀"
        )

        # 👉 ждём сообщение пользователя
        user_data[user_id]["wait_refs"] = True
        return

# ▶️ запуск
async def main():
    print("🚀 BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())