# Проект автоматизации тестирования API приложения для заказа космических бургеров
* Основа для написания автотестов — фреймворки pytest и selenium, а также библиотека requests
* Команда для запуска тестов — pytest -v
* Собрать отчёт о тестировании - pytest tests*test_name.py --alluredir=allure_results
* Посмотреть наглядно отчёт можно с помощью команды allure serve allure_results
* в data.py описаны текста сообщений ответов API запросов, а также тело запроса с валидными ингридиентами
* в helpers.py реализован генератор кредов для аккаунта