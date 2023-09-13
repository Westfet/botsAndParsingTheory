import redis
import json

# создаем объект класса Redis - нашу базу данных
red = redis.Redis(
    host='redis-17566.c299.asia-northeast1-1.gce.cloud.redislabs.com',
    port=17566,
    password='RJDdUB5wFOb7A8XxmeSXc9m31c5rgx7m'
)

# для проверки подключения в терминале пишем: python -i redis_caching.py -> enter -> имя бд

# для того, чтобы записать данные в кэш, используется метод .set('название переменной для
# хеширования','значение переменной в виде строки')

red.set('var2', 'value2')
print(red.get('var2'))

# запишем словарь

# создаем словарь для записи
dict1 = {'key1': 'value1', 'key2': 'value2'}
# с помощью функции dumps() из модуля json превратим словарь в строчку
red.set('dict1', json.dumps(dict1))
# с помощью функции .loads() превращаем данные, полученные из кэша обратно в словарь
converted_dict = json.loads(red.get('dict1'))
print(type(converted_dict))
print(converted_dict)

# удаление данных по ключу с помощью метода .delete()
red.delete('dict1')
print(red.get('dict1'))


