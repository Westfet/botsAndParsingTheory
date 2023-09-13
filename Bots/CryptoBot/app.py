import telebot
from config import TOKEN, keys
from utils import ConversionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


# сообщение при вводе команд "/start" или "/help"
@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:' \
           '<имя валюты>' \
           '<в какую валюту перевести>' \
           '<количество переводимой валюты> \n' \
           'Увидеть список всех доступных валют: /values'

    bot.reply_to(message, text)


# команда с допустимыми валютами
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# обработка запроса от пользователя
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversionException('Некорректно введены параметры.')
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка ввода данных.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
