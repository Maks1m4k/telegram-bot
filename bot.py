import telebot
from telebot import types

API_TOKEN = "7995822806:AAFxMXRSjIQdZT6HLxjg_6xXL3ikMBCzRU8"
ADMIN_ID = 7351723829

bot = telebot.TeleBot(API_TOKEN)

# Кнопки після /start
def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📨 Написати адміну")
    btn2 = types.KeyboardButton("📢 Надіслати новину / слух")
    keyboard.add(btn1)
    keyboard.add(btn2)
    return keyboard

# Команда /start
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "👋 Вітаю! Оберіть, що хочете зробити:",
        reply_markup=main_keyboard()
    )

# Обробка натискання кнопок
@bot.message_handler(func=lambda message: message.text in ["📨 Написати адміну", "📢 Надіслати новину / слух"])
def handle_buttons(message):
    if message.text == "📨 Написати адміну":
        bot.send_message(
            message.chat.id,
            "✉️ Напишіть повідомлення адміну нижче — і він вам відповість."
        )
        bot.register_next_step_handler(message, handle_admin_message)
    elif message.text == "📢 Надіслати новину / слух":
        bot.send_message(
            message.chat.id,
            "📰 Напишіть слух або новину, яку хочете передати. Анонімність гарантуємо."
        )
        bot.register_next_step_handler(message, handle_news_message)

# Повідомлення адміну
def handle_admin_message(message):
    text = f"📩 <b>Нове повідомлення адміну</b>\n\n"
    text += f"👤 Від: @{message.from_user.username or 'Без ніку'}\n"
    text += f"🆔 ID: <code>{message.from_user.id}</code>\n\n"
    text += f"💬 Текст: {message.text}"
    
    markup = types.InlineKeyboardMarkup()
    reply_btn = types.InlineKeyboardButton("💭 Відповісти", callback_data=f"reply_{message.from_user.id}")
    markup.add(reply_btn)
    
    bot.send_message(ADMIN_ID, text, parse_mode="HTML", reply_markup=markup)
    bot.send_message(message.chat.id, "✅ Повідомлення надіслано адміну!")

# Новини / слухи
def handle_news_message(message):
    text = f"📢 <b>Надіслано новину / слух</b>\n\n"
    text += f"👤 Від: @{message.from_user.username or 'Без ніку'}\n"
    text += f"🆔 ID: <code>{message.from_user.id}</code>\n\n"
    text += f"📰 Текст: {message.text}"
    
    markup = types.InlineKeyboardMarkup()
    reply_btn = types.InlineKeyboardButton("💭 Відповісти", callback_data=f"reply_{message.from_user.id}")
    markup.add(reply_btn)
    
    bot.send_message(ADMIN_ID, text, parse_mode="HTML", reply_markup=markup)
    bot.send_message(message.chat.id, "✅ Ваш слух / новину відправлено адміну!")

# Коли адмін натискає "Відповісти"
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def reply_to_user(call):
    user_id = int(call.data.split("_")[1])
    msg = bot.send_message(ADMIN_ID, "✏️ Напиши повідомлення, яке хочеш відправити користувачу:")
    bot.register_next_step_handler(msg, send_reply, user_id)

def send_reply(message, user_id):
    bot.send_message(user_id, f"💬 Відповідь адміністратора:\n{message.text}")
    bot.send_message(ADMIN_ID, "✅ Відповідь надіслано користувачу.")

# Запуск бота
bot.polling(none_stop=True)
