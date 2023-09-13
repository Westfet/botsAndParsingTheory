import telebot
from config import TOKEN
import sqlite3

bot = telebot.TeleBot(TOKEN)
name = None


# пример работы с базой данных

@bot.message_handler(commands=['go'])
def go(message: telebot.types.Message):
    # создание бд и установка соединения с ней (сокращение от connect)
    conn = sqlite3.connect('users.sql')
    # создание объекта, позволяющего выполнять различные команды, связанные с БД (cur от cursor)
    cur = conn.cursor()
    # подготовка таблицы для записи пользователей, метод .execute позволяет вводить sql запросы
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, '
                'name varchar(50), pass varchar(50))')
    # выполняем создание таблицы
    conn.commit()
    # закрытие объекта и бд после создания таблицы
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем!''\n'
                                      'Введите имя пользователя:')
    # следующим шагом вызовем функцию, она будет получать имя пользователя
    bot.register_next_step_handler(message, user_name)


def user_name(message: telebot.types.Message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль:')
    # вызываем функцию, которая будет получать пароль от пользователя и заносить его в БД
    bot.register_next_step_handler(message, user_pass)


def user_pass(message: telebot.types.Message):
    password = message.text.strip()
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    # добавление в таблицу базы данных нового юзера
    cur.execute("INSERT INTO users (name, pass) VALUES ('%s','%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()
    # создание кнопки со списком всех пользователей
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!!!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call: telebot.types.CallbackQuery):
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    # запрашиваем все элементы из таблицы
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    # перебор всех строчек таблицы и запись нужной информации в пустую строку 'info'
    for item in users:
        info += f"Имя: {item[1]} \n"
    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)


bot.polling(none_stop=True)
