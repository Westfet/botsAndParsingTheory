# JSON (JavaScript Object Notation) - самый популярный текстовый формат обмена данными.
# JSON очень похож на словарь в python. Для работы с JSON файлами в python есть модуль json

# Основные методы:
# 1. json.loads(JSON строка) создает словарь python из JSON строки
# 2. json.dumps(python obj, indent=) создает JSON строку из объекта python (indent кол-во отступов)
# 3. json.dump(python obj, файл сохранения, indent=) создает JSON строку и сохраняет ее в файл
# 4. json.load(JSON файл) создает словарь python из JSON файла


import json
from random import randint

# строка в JSON формате
str_json = """
{
    "persons": {
        "count" : 2,
        "items" : [{
            "id": 210700286,
            "first_name": "Lindsey",
            "last_name": "Stirling",
            "sex" : "female",
            "age" : "36",
            "height" : "1.61"
        }, {
            "id": 297428682,
            "first_name": "Jared",
            "last_name": "Leto",
            "sex" : "male",
            "age" : "51",
            "height" : "1.80"
        }]
    }
}"""

# преобразование JSON строки в объекты python
data = json.loads(str_json)

# на выходе получаем словарь python
print(type(data), "\n")

# получим внутреннее содержимое словаря "persons"
print(data['persons'], "\n")

# получим внутреннее содержимое словаря "items", находящегося внутри словаря "persons"
print(data['persons']['items'], "\n")

# значения словаря "items" являются списком, его можно проитерировать
for item in data['persons']['items']:
    # значения словаря items являются словарями, с которыми мы можем работать по ключу
    print(item['first_name'], item['last_name'])
    # добавление / удаление элементов в существующем JSON файле
    del item['id']
    item['likes'] = randint(1000, 5000)

print("\n", data['persons']['items'], "\n")

# создание JSON строки из объекта python, indent задает количество отступов
new_json = json.dumps(data, indent=4)
print(new_json)

# создадим файл и сохраним туда наш словарь
with open('my.json', 'w') as file:
    json.dump(data, file, indent=4)

# откроем созданный файл и сохраним его как python объект
with open('my.json', 'r') as file:
    data = json.load(file)


