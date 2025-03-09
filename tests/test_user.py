import pytest
import allure
import requests
import time
from data import AppResponseMessages
from helpers import generate_uniq_creds
from urls import AppUrls


class TestUserCreate:

    @allure.title('Регистрация уникального пользователя')
    @allure.description('Регистрируем новый аккаунт с свободной почтой и сверяем код и текст ответа')
    def test_user_create_unique_user(self):
        payload = generate_uniq_creds()
        response = requests.post(AppUrls.user_create_url, data=payload)
        assert response.status_code == 200
        assert AppResponseMessages.success_message in response.text

        #удаление юзера после теста
        token = response.json()['accessToken']
        auth_data = {
            "email": payload['email'],
            "password": payload['password']
            }
        requests.post(AppUrls.login_url, data=auth_data, headers={'accessToken': token})
        requests.delete(AppUrls.user_info_url, headers={'authorization': token})

    @allure.title('Регистрация существующего пользователя')
    @allure.description('Дважды отправляем запрос на регистрацию с одинаковыми данными, сверяем код и текст ошибки')
    def test_user_create_existing_user(self):
        payload = generate_uniq_creds()
        requests.post(AppUrls.user_create_url, data=payload)
        response = requests.post(AppUrls.user_create_url, data=payload)
        assert response.status_code == 403
        assert AppResponseMessages.user_exists_error in response.text

    @allure.title('Регистрация пользователя с пустым обязательным полем')
    @allure.description('Отправляем запрос с пустым обязательным полем. Пустое поле подменяется с помощью параметризации')
    @pytest.mark.parametrize('required_field', ['email', 'password', 'name'])
    def test_user_create_empty_required_fields(self, required_field):
        payload = generate_uniq_creds()
        payload.pop(required_field)
        response = requests.post(AppUrls.user_create_url, data=payload)
        assert response.status_code == 403
        assert AppResponseMessages.required_fields_error in response.text

class TestUserLogin:

    @allure.title('Логин в аккаунт')
    @allure.description('Совершаем вход в созданный аккаунт с валидными данными')
    def test_user_login_existing_user(self, create_login_delete_account):
        valid_creds, _, __, token = create_login_delete_account

        auth_data = {
            "email": valid_creds['email'],
            "password": valid_creds['password']
        }

        response_login = requests.post(AppUrls.login_url, data=auth_data, headers={'accessToken': token})

        assert response_login.status_code == 200
        assert valid_creds['email'] in response_login.text

    @allure.title('Логин в аккаунт с невалидными данными')
    @allure.description('Совершаем вход в аккаунт с невалидным email/паролем')
    @pytest.mark.parametrize('wrong_data', ['email', 'password'])
    def test_user_login_invalid_creds(self, create_login_delete_account, wrong_data):
        valid_creds, _, __, token = create_login_delete_account

        valid_creds[wrong_data] = 'amogus' #по очереди заменяем email и пароль на невалидные

        auth_data = {
            "email": valid_creds['email'],
            "password": valid_creds['password']
        }

        response_login = requests.post(AppUrls.login_url, data=auth_data, headers={'accessToken': token})

        assert response_login.status_code == 401
        assert AppResponseMessages.invalid_creds_error in response_login.text

class TestUserUpdateData:

    @allure.title('Обновление информации авторизаванного пользователя')
    @allure.description('Обновляем email/пароль/имя авторизованного пользователя')
    @pytest.mark.parametrize('update_data', ['email', 'password', 'name'])
    def test_user_update_data_with_auth(self, create_login_delete_account, update_data):
        valid_creds, _, __, token = create_login_delete_account

        valid_creds[update_data] = int(time.time()) #изменяем значение одного из полей на уникальное новое

        data_to_update = {
            "email": valid_creds['email'],
            "password": valid_creds['password'],
            "name": valid_creds['name']
        }

        update_response = requests.patch(AppUrls.user_info_url, data=data_to_update, headers={'authorization': token})

        assert update_response.status_code == 200
        assert AppResponseMessages.success_message in update_response.text

    @allure.title('Обновление информации неавторизованного пользователя')
    @allure.description('Обновляем email/пароль/имя неавторизованного пользователя. Сверяем код и текст ошибки')
    @pytest.mark.parametrize('update_data', ['email', 'password', 'name'])
    def test_user_update_data_without_auth(self, create_login_delete_account, update_data):
        valid_creds, _, __, ___ = create_login_delete_account
        valid_creds[update_data] = int(time.time())  # изменяем значение одного из полей на уникальное новое

        data_to_update = {
            "email": valid_creds['email'],
            "password": valid_creds['password'],
            "name": valid_creds['name']
        }

        #делаем запрос на изменение информации без передачи токена, т.е. без авторизации
        update_response = requests.patch(AppUrls.user_info_url, data=data_to_update, headers={'authorization': ""})

        assert update_response.status_code == 401
        assert AppResponseMessages.no_auth_error in update_response.text
