import pytest
import requests
from helpers import generate_uniq_creds
from urls import AppUrls
from data import IngredientsData

@pytest.fixture()
def create_login_delete_account():
    valid_creds = generate_uniq_creds() #генерируем уникальные email, password, name

    response_create = requests.post(AppUrls.user_create_url, data=valid_creds) #создаём акк

    #токен и тело запроса для логина
    token = response_create.json()['accessToken']
    auth_data = {
        "email": valid_creds['email'],
        "password": valid_creds['password']
    }

    #логин
    response_login = requests.post(AppUrls.login_url, data=auth_data, headers={'accessToken': token})

    yield valid_creds, response_create, response_login, token

    requests.delete(AppUrls.user_info_url, headers={'authorization': token}) #удаление акка после тестов

@pytest.fixture()
def create_order(create_login_delete_account):
    _, __, ___, token = create_login_delete_account

    requests.post(AppUrls.order_url, data=IngredientsData.PAYLOAD, headers={'authorization': token})

    return token
