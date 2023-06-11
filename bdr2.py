import telebot
import openai

# Конфігурація OpenAI API
openai.api_key = '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'

# Конфігурація токену вашого Telegram-бота
bot = telebot.TeleBot('6156987762:AAE5OJcoAOCDsuitVCpatjqoTmeC30hBTP0')

# Словник з темами та підтемами
# Словник з темами та підтемами
topics = {
    'Розвідка': ['Сканування nmap', 'Google dorks'],
    'Виявлення вразливостей': ['Тестування на проникнення', 'XSS-атаки'],
    'Pen-testing': ['Тестування коду на вразливість', 'ше шось', 'ше шось'],
    'Політика безпеки': ['Тестування на проникнення', 'XSS-атаки']
}

# Обробник команди /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in topics.keys():
        keyboard.add(topic)
    bot.reply_to(message, 'Виберіть тему:', reply_markup=keyboard)

# Обробник вибору теми
@bot.message_handler(func=lambda message: message.text in topics.keys())
def handle_topic(message):
    topic = message.text
    subtopics = topics[topic]
    if subtopics:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subtopic in subtopics:
            keyboard.add(subtopic)
        bot.reply_to(message, 'Виберіть підтему:', reply_markup=keyboard)
    else:
        bot.reply_to(message, 'Обробка запиту з теми: ' + topic)
        bot.reply_to(message, 'Введіть запит, який стосується даної теми:')

# Обробник вибору підтеми
@bot.message_handler(func=lambda message: message.text in sum(topics.values(), []))
def handle_subtopic(message):
    subtopic = message.text
    bot.reply_to(message, 'Обробка запиту з підтеми: ' + subtopic)
    bot.reply_to(message, 'Введіть запит, який стосується даної підтеми:')

# Обробник введеного запиту
@bot.message_handler(func=lambda message: True)
def handle_query(message):
    query = message.text
    # Виклик GPT для отримання відповіді
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt='Відповідай на запит',
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7
    )
    bot.reply_to(message, 'Відповідь GPT: ' + response.choices[0].text.strip())

# Запуск бота
bot.polling()