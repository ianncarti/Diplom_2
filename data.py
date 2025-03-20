class AppResponseMessages:

    #регистрация аккаунта
    SUCCESS_MESSAGE = '"success":true'
    USER_EXISTS_ERROR = 'User already exists'
    REQUIRED_FIELDS_ERROR = 'Email, password and name are required fields'

    #логин
    INVALID_CREDS_ERROR = "email or password are incorrect"

    #обновление информации о пользователе
    NO_AUTH_ERROR = "You should be authorised"

    #заказы
    ORDER_NUMBER = '"number":'
    NEED_INGREDIENTS_ERROR = "Ingredient ids must be provided"
    WRONG_INGREDIENTS_ERROR = 'Internal Server Error'

class IngredientsData:
    #id ингридиентов для заказа
    PAYLOAD = {"ingredients": ["61c0c5a71d1f82001bdaaa6d","61c0c5a71d1f82001bdaaa6f"]}

