import telebot
from telebot import types
# модуль для открытия web страниц
import webbrowser

from config import TOKEN

bot = telebot.TeleBot(TOKEN)


# Код читается программой сверху вниз, поэтому логичнее вверху помещать обработки команд
@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    # чтобы изменить написание текста, нужно воспользоваться атрибутом parse_mod(='html')
    # считывает написанные теги html вокруг текста
    # bot.send_message(message.chat.id, '<b><em><u>Привет!!</u></em></b>', parse_mode='html')

    # если нужно вывести информацию о чате и о пользователе, то в скобке у метода нужно передать
    # объект функции(message) и нужный атрибут (у объекта есть куча атрибутов!!!)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} '
                                      f'{message.from_user.last_name}')


# чтобы добавить команды в интерфейс бота, переходим к BotFather и отправляем команду '/setcommands'
# и следуем инструкциям - работу команды прописываем здесь, регистрируем ее у BotFather,
# зарегистрированная команда появится в меню бота
@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://translate.google.com')


# создание встроенных кнопок - тех кнопок, которые отображаются после самого сообщения
@bot.message_handler(commands=['value'])
def value(message: telebot.types.Message):
    text = 'Выберите нужный вариант: '
    # вызываем экземпляр класса для создания встроенных кнопок
    markup = types.InlineKeyboardMarkup()
    # создание кнопок - - в скобках для кнопки указываем описание(текст) и действие
    btn1 = types.InlineKeyboardButton('Переход на сайт', url='https://translate.google.com')
    # чтобы какую-либо функцию после нажатия на кнопку - прописываем функцию в callback_data
    btn2 = types.InlineKeyboardButton('Удаление предыдущего сообщения', callback_data='delete')
    # расположение 2-х кнопок на одном ряду (по умолчанию на одном ряду одна кнопка)
    markup.row(btn1, btn2)
    # команда bot.reply_to отправляет ответ и в шапку помещает сообщение, на которое отвечает
    bot.reply_to(message, text, reply_markup=markup)


# обработчик нажатия кнопки btn2
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback: telebot.types.CallbackQuery):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)


# создание кнопок, которые будут отображаться при вводе текста
@bot.message_handler(commands=['help'])
def help_command(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на сайт')
    btn2 = types.KeyboardButton('Список валют')
    markup.row(btn1)
    markup.row(btn2)
    bot.send_message(message.chat.id, 'Действия:', reply_markup=markup)
    # кнопки при вводе текста - это заготовленный текст, после которого будет что-то происходить
    # сейчас мы отдадим команду боту на выполнение следующего зна нажатием кнопки действия (
    # on_click - функция, которая будет обрабатывать кнопки)
    bot.register_next_step_handler(message, on_click)


# обработка текста с кнопок
def on_click(message: telebot.types.Message):
    if message.text == 'Перейти на сайт':
        webbrowser.open('https://translate.google.com')
    elif message.text == 'Список валют':
        bot.send_message(message.chat.id, 'Доллар, Евро, Рубль')


# передача файлов пользователю - пример с фото, с другими типами файлов аналогично (аудио, видео)
@bot.message_handler(commands=['calendar'])
def give_calendar(message: telebot.types.Message):
    # второй аргумент - способ открытия файла (rb - на чтение)
    file = open('img/photo.png', 'rb')
    bot.send_photo(message.chat.id, file)


bot.polling(none_stop=True)
