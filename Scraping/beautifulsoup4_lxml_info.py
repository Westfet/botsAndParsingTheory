# Библиотека Beatifulsoup - швейцарский нож при написании web парсеров, с помощью нее можно
# разобрать на "винтики" полученную нами web-страницу
import re

from bs4 import BeautifulSoup

with open('blank/index2.html', encoding="utf-8") as file:
    src = file.read()
# чтобы пользоваться методами Beatifulsoup, необходимо "скормить" наш код библиотеке
# сделать это можно, создав экземпляр класса, который в качестве аргументов принимает код и
# парсер(lxml), с помощью которого будет осуществлено преобразование

soup = BeautifulSoup(src, "lxml")

# I. Основные МЕТОДЫ библиотеки - .find() и .find_all(), которые ищут нужный нам элемент сверху
# вниз, опускаясь вглубь кода. Используются они по-разному

# №1. Поиск по тегу

# .find() - найдет и сохранит в переменную 1-й попавшиеся элемент с нужным нам тегом
page_h1 = soup.find("h1")
print(page_h1, "\n")

# .find_all() - найдет и сохранит в переменную все элементы с нужным нам тегом в список
page_all_h1 = soup.find_all("h1")
print(page_all_h1, "\n")

# .find_all() - вернет нам список, который можно проитерировать, обращаться к элементу списка
for i in page_all_h1:
    # если нам нужно только содержимое без тегов, добавляем к элементу .text
    print(i.text, "\n")

# помимо поиска по тегу мы можем сделать запрос, используя атрибуты тега, например, класс
user_name = soup.find("div", class_="user__name")
# таким образом мы получили весь блок div целиком
print(user_name, "\n")
# однако это не просто блок div, а элемент класса BS4, к которому можно применить различные методы
print(user_name.text.strip(), "\n")

# можно также продвигаться вглубь кода за нужной информацией
print(soup.find("div", class_="user__name").find("span").text.strip(), "\n")

#  №2. Помимо поиска по тегу мы можем при поиске передавать словарь, в котором с помощью пар
#  ключ-значение мы указываем параметры отбора

#  удобство метода заключается в том, что при необходимости тщательного отбора мы можем
#  передавать несколько атрибутов, если какой-то из атрибутов будет не найдет, выпадет ошибка
user_name1 = soup.find("div", {"class": "user__name", "id": "aaa"}).find("span")

# сбор всех "span" из класса user__info"
find_all_spans_in_user_info = soup.find(class_="user__info").find_all("span")
print(find_all_spans_in_user_info, "\n")
for item in find_all_spans_in_user_info:
    print(item.text)

# Спарсим ссылки на соц.сети, пройдясь вглубь по тегам
social_links = soup.find(class_="social__networks").find("ul").find_all("a")
for item in social_links:
    # ссылка всегда хранится в атрибуте href, получим при помощи метода .get("href")
    item_url = item.get("href")
    item_text = item.text
    print(f"{item_text} - {item_url}")

# II. МЕТОДЫ .find_parent() и .find_parents() - ищут родителя(ей) этого элемента,
# т.е. поднимаются по структуре html дерева снизу вверх

post_div = soup.find(class_="post__text").find_parent()
# мы забираем блок не целиком, а до первого родителя, двигаясь снизу вверх
print(post_div)

# передадим параметры поиска в метод .find_parent - укажем родителя, расположенного по иерархии выше
post_div = soup.find(class_="post__text").find_parent("div", "user__post")
print(post_div)

# метод .find_parents работает так, что поднимается снизу вверх до тега html. Передавая параметры
# в скобках мы ограничиваем поднятие вверх
post_divs = soup.find(class_="post__text").find_parents("div", "user__post")
print(post_divs, "\n")

# III. МЕТОДЫ .next_element  .previous_element, find_next,find_previous полезны при перемещении по
# коду

# важное уточнение - .next_element и previous_element работают дотошно и может вернуть не сам
# элемент, а перенос строки перед элементом, для того, чтобы все сработало, пишем .next_element
# два раза
next_el = soup.find(class_="post__title").next_element.next_element.text
print(next_el)

# find_next и find_previous сразу вернут нам элемент
next_ell = soup.find(class_="post__title").find_next().text
print(next_ell)

# IV. МЕТОДЫ .find_next_sibling() и .find_previous_sibling() ищут и возвращают элементы внутри тега
next_sib = soup.find(class_="post__title").find_next_sibling()
print(next_sib)

# Комбинация различных методов между собой
post_title = soup.find(class_="post__title").find_next_sibling().find_next().text
print(post_title)

# Как забрать атрибуты из тегов
links = soup.find(class_="some__links").find_all("a")
for link in links:
    # парсить атрибуты можно не только с помощью метода .get, но и напрямую обращаясь к ссылке
    link_href_attr = link["href"]
    link_data_attr = link["data-attr"]
    print(link_href_attr)
    print(link_data_attr)

# Мы можем искать элементы, передавая в параметр текст, но BS4 осуществляет поиск только по
# полному содержанию, а не по отдельному слову или символу.
# Прокачать BS4 можно, используя модуль регулярных выражений "re"

find_a_by_text = soup.find("a", text=re.compile("Одежда"))
print(find_a_by_text)

# можно также найти слово с первой буквой в верхнем и нижнем регистрах
find_all_clothes = soup.find_all(text=re.compile("([Оо]дежда)"))
print(find_all_clothes)

