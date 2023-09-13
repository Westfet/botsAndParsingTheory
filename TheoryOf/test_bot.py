import telebot

# инициализация бота
TOKEN = "5932432243:AAGsa_lAkV58yhE7D1MBrSS5RsfkGMxUWxA"
bot = telebot.TeleBot(TOKEN)


# Обработчики сообщений. Обработчик сообщений - это функция, которая будет выполняться при
# получении определенного сообщения. Обработчики сообщений обычно состоят из одного или
# нескольких фильтров

# Для того, чтобы из обычной функции сделать обработчик сообщений для бота надо воспользоваться
# декоратором @bot.message_handler() or @bot.message_handler(filters).

# Повтор сообщения от пользователя
# @bot.message_handler()
# def repeat(message: telebot.types.Message):
#     bot.send_message(message.chat.id, message.text)


# filters - фильтры, определяющие, следует ли вызывать декорированную функцию для
# соответствующего сообщения или нет; фильтров может быть несколько. Два основных фильтра:
#   1. Тип контента
#       название - content_types
#       аргумент - список строк, по умолчанию ['text']
#       условие выполнения - если тип контента совпадает с указанным в скобках
#   2. Команды
#       название - commands
#       аргумент - список строк
#       условие выполнения - если сообщение начинается с команды, указанной в списке

# Ответ на голосовые сообщения
@bot.message_handler(content_types=['voice'])
def voice_message_answer(message: telebot.types.Message):
    bot.send_message(message.chat.id, "У тебя очень красивый голос!")


# Приветственное сообщение при запуске бота
@bot.message_handler(commands=['start', 'help'])
def greetings(message):
    bot.send_message(message.chat.id, f"Welcome, {message.chat.username}")


bot.polling(none_stop=True)  # запуск бота
