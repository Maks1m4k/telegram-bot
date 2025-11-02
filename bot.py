import telebot
import os

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(API_TOKEN)

# 🔹 Коли користувач пише боту
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID, content_types=['text', 'photo', 'document'])
def forward_to_admin(message):
    # Якщо є текст
    if message.text:
        bot.send_message(ADMIN_ID, f"📩 Повідомлення від @{message.from_user.username or 'немає username'} "
                                   f"(ID: {message.chat.id}):\n\n{message.text}")
    # Якщо є фото
    elif message.photo:
        file_id = message.photo[-1].file_id
        caption = message.caption or ""
        bot.send_photo(ADMIN_ID, file_id, caption=f"📷 Фото від (ID: {message.chat.id})\n\n{caption}")
    # Якщо є документ
    elif message.document:
        file_id = message.document.file_id
        caption = message.caption or ""
        bot.send_document(ADMIN_ID, file_id, caption=f"📎 Документ від (ID: {message.chat.id})\n\n{caption}")

# 🔹 Команда для відповіді
@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    try:
        parts = message.text.split(' ', 2)
        if len(parts) < 3:
            bot.reply_to(message, "❗ Формат: /reply <user_id> <текст>")
            return

        user_id = int(parts[1])
        text = parts[2]

        bot.send_message(user_id, f"💬 Відповідь від адміністратора:\n\n{text}")
        bot.reply_to(message, f"✅ Відповідь надіслана користувачу {user_id}")

    except Exception as e:
        bot.reply_to(message, f"❌ Помилка: {e}")

bot.infinity_polling()
