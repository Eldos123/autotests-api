import allure  # Импортируем allure
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema, UserSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger  # Импортируем функцию для создания логгера

logger = get_logger("USERS_ASSERTIONS")  # Создаем логгер с именем "USERS_ASSERTIONS"


@allure.step("Check create user response")  # Добавили allure шаг
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Проверяет, что ответ на создание пользователя соответствует запросу.
    :param request: Исходный запрос на создание пользователя.
    :param response: Ответ API с данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check create user response")

    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")

@allure.step("Check user")  # Добавили allure шаг
def assert_user(actual: UserSchema, expected: UserSchema):
    """
    Проверяет корректность данных пользователя, сравнивая два объекта UserSchema.
    :param actual: Фактические данные пользователя.
    :param expected: Ожидаемые данные пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check user")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")


@allure.step("Check get user response")  # Добавили allure шаг
def assert_get_user_response(get_user_response: GetUserResponseSchema, create_user_response: CreateUserResponseSchema):
    """
    Проверяет, что данные пользователя из ответа на запрос совпадают с данными при создании.
    :param get_user_response: Ответ API при запросе пользователя.
    :param create_user_response: Ответ API при создании пользователя.
    :raises AssertionError: Если данные пользователя не совпадают.
    """
    logger.info("Check get user response")

    assert_user(actual=get_user_response.user, expected=create_user_response.user)