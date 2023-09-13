import requests


# Получение ссылок на фотографии по ключевым словам - функция download

def download(q: str, p: str):
    # чтобы запрос прошел, необходимо указать авторизацию
    header = {"Authorization": "VNbjilDa0ivST54HyQtlMCj9wkuUA1PLwjSDK9UgQHUx7xTrskwInUTZ"}
    i = 1
    # "p" будет отвечать за количество страниц, которые мы будем обрабатывать
    while i <= int(p):
        # адрес сайта с интегрированным туда ключевым словом, которое передает пользователь
        url = f"https://api.pexels.com/v1/search?query={q}&per_page=1&page={i}"
        # формирование GET HTTP запроса при помощи библиотеки requests
        r = requests.get(url, headers=header)
        # Проверка на ошибки - код 200 означает, что все хорошо
        if r.status_code == 200:
            # преобразование полученного ответа в .json формат
            _r = r.json()
            # пройдемся циклом for по данным из значения, полученного по ключу (в примере значение
            # ключа "photos" - это словарь
            for item in _r.get("photos"):
                # по ключу внутри словаря находим ссылку на фотографию с ключевым словом
                print(item.get("url"))
        else:
            print(r.status_code)
        i += 1


def main() -> None:
    q = input("Query ")
    p = input("Count page ")
    download(q, p)


main()
