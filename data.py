class AppResponseMessages:

    #регистрация аккаунта
    success_message = '"success":true'
    user_exists_error = 'User already exists'
    required_fields_error = 'Email, password and name are required fields'

    #логин
    invalid_creds_error = "email or password are incorrect"

    #обновление информации о пользователе
    no_auth_error = "You should be authorised"

    #заказы
    order_number = '"number":'
    need_ingredients_error = "Ingredient ids must be provided"
    wrong_ingredients_error = 'Internal Server Error'

class IngredientsData:
    #id ингридиентов для заказа
    payload = {"ingredients": ["61c0c5a71d1f82001bdaaa6d","61c0c5a71d1f82001bdaaa6f"]}

