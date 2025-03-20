import time


#метод генерирует уникальные креды на основе текущей даты и возвращает тело запроса для регистрации
def generate_uniq_creds(base_name="user"):
    timestamp = int(time.time())  # Получаем текущее время в секундах
    payload = {'email': f"{base_name}_{timestamp}@yandex.ru", 'password': f"{base_name}_{timestamp}",
               'name': f"{base_name}_{timestamp}"}
    return payload
