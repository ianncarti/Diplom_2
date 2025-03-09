import allure
import requests
from data import IngredientsData, AppResponseMessages
from urls import AppUrls


class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией')
    @allure.description('Создаём заказ залогиненным юзером. Сверяем код и текст ответа')
    def test_create_order_with_auth(self, create_login_delete_account):
        _, __, ___, token = create_login_delete_account

        create_order_response = requests.post(AppUrls.order_url, data=IngredientsData.payload,
                                              headers={'authorization': token})

        assert create_order_response.status_code == 200
        assert AppResponseMessages.order_number in create_order_response.text

    @allure.title('Создание заказа с без авторизации')
    @allure.description('Создаём заказ незалогиненным юзером. Сверяем код и текст ошибки')
    def test_create_order_no_auth(self):
        create_order_response = requests.post(AppUrls.order_url, data=IngredientsData.payload)

        assert create_order_response.status_code == 200
        assert AppResponseMessages.order_number in create_order_response.text

    @allure.title('Создание заказа без ингридиентов')
    @allure.description('Создаём заказ без тела запроса. Сверяем код и текст ошибки')
    def test_create_order_without_ingredients(self, create_login_delete_account):
        _, __, ___, token = create_login_delete_account

        create_order_response = requests.post(AppUrls.order_url, headers={'authorization': token})

        assert create_order_response.status_code == 400
        assert AppResponseMessages.need_ingredients_error in create_order_response.text

    @allure.title('Создание заказа с невалидными ингридиентами')
    @allure.description('Создание заказа с невалидным id ингридиентов в теле запроса')
    def test_create_order_wrong_ingredient_hash(self, create_login_delete_account):
        _, __, ___, token = create_login_delete_account

        wrong_ingredients_payload = {"ingredients": ["amogus","booba"]}

        create_order_response = requests.post(AppUrls.order_url, data=wrong_ingredients_payload,
                                              headers={'authorization': token})

        assert create_order_response.status_code == 500
        assert AppResponseMessages.wrong_ingredients_error in create_order_response.text


class TestGetOrder:

    @allure.title('Получение заказа авторизованного юзера')
    @allure.description('Получаем список заказов авторизованного юзера. Сверяем код и текст ответа')
    def test_get_order_with_auth(self, create_order):
        token = create_order

        get_order_response = requests.get(AppUrls.order_url, headers={'authorization': token})

        assert get_order_response.status_code == 200
        assert AppResponseMessages.success_message in get_order_response.text

    @allure.title('Получение заказа юзера без авторизации')
    @allure.description('Отправляем запрос на получение заказа без передачи токена. Сверяем код и текст ошибки')
    def test_get_order_without_auth(self, create_order):
        get_order_response = requests.get(AppUrls.order_url, headers={'authorization': ""})

        assert get_order_response.status_code == 401
        assert AppResponseMessages.no_auth_error in get_order_response.text
