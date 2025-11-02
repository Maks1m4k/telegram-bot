import telebot

# 🔑 Твій токен
API_TOKEN = '7995822806:AAFxMXRSjIQdZT6HLxjg_6xXL3ikMBCzRU8'

# 🔸 Твій Telegram ID
ADMIN_ID = 7351723829  # заміни на свій

bot = telebot.TeleBot(API_TOKEN)
user_messages = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Написати адміну', 'Відправити слух/новину')
    bot.send_message(
        message.chat.id,
        "👋 Вітаю!\nХочете написати адміну, чи маєте якийсь слух або новину?\n"
        "Пишіть нам у бота — анонімність гарантуємо ✅\n\n"
        "Оберіть одну з опцій нижче 👇",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'voice', 'document'])
def handle_messages(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    if message.text == 'Написати адміну':
        bot.send_message(user_id, "✉️ Напишіть повідомлення адміну нижче, і він вам відповість.")
        user_messages[user_id] = {'type': 'admin'}
        return
    elif message.text == 'Відправити слух/новину':
        bot.send_message(user_id, "📰 Напишіть слух або новину, яку хочете передати.\nАнонімність гарантуємо ✅")
        user_messages[user_id] = {'type': 'news'}
        return

    if user_id in user_messages:
        msg_type = user_messages[user_id]['type']

        # Створюємо повідомлення для адміна
        text = f"📩 Повідомлення від [{username}] (ID: {user_id}):"
        if msg_type == 'admin':
            text = f"✉️ [{username}] написав адміну:"
        elif msg_type == 'news':
            text = f"🗞 Новина/слух від [{username}]:"

        # Надсилаємо контент
        if message.content_type == 'text':
            bot.send_message(ADMIN_ID, f"{text}\n{message.text}")
        elif message.content_type == 'photo':
            bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=text)
        elif message.content_type == 'video':
            bot.send_video(ADMIN_ID, message.video.file_id, caption=text)
        elif message.content_type == 'voice':
            bot.send_voice(ADMIN_ID, message.voice.file_id, caption=text)
        elif message.content_type == 'document':
            bot.send_document(ADMIN_ID, message.document.file_id, caption=text)

        bot.send_message(user_id, "✅ Ваше повідомлення надіслано.")
        del user_messages[user_id]

    elif user_id == ADMIN_ID and message.text and message.text.startswith('/reply'):
        try:
            parts = message.text.split(' ', 2)
            target_id = int(parts[1])
            reply_text = parts[2]
            bot.send_message(target_id, f"📩 Відповідь від адміна:\n{reply_text}")
            bot.send_message(ADMIN_ID, "✅ Відповідь відправлено.")
        except Exception:
            bot.send_message(ADMIN_ID, "⚠️ Неправильний формат. Використовуйте:\n/reply ID текст")

bot.infinity_polling()
