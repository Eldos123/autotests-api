import allure  # Импортируем allure

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, ExerciseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, \
    GetExercisesResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response
from tools.logger import get_logger  # Импортируем функцию для создания логгера

logger = get_logger("EXERCISE_ASSERTIONS")  # Создаем логгер с именем "COURSES_ASSERTIONS"

@allure.step("Check create exercise response")  # Добавили allure шаг
def assert_create_exercise_response(request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
    """
    Проверяет соответствие ответа на создание задания данным запроса.
    :param request: Схема запроса для создания задания
    :param response: Схема ответа, полученного от API
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Check create exercise response")

    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")

@allure.step("Check exercise")  # Добавили allure шаг
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные задания соответствуют ожидаемым.

    :param actual: Фактические данные задания
    :param expected: Ожидаемые данные задания
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    logger.info("Check exercise")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

@allure.step("Check get exercise response")  # Добавили allure шаг
def assert_get_exercise_response(actual: GetExerciseResponseSchema, expected: ExerciseSchema):
    """
    Проверяет, что ответ на получение задания соответствует ожидаемым данным.

    :param actual: Фактический ответ API
    :param expected: Ожидаемые данные задания
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    logger.info("Check get exercise response")

    assert_exercise(actual.exercise, expected)

@allure.step("Check update exercise response")  # Добавили allure шаг
def assert_update_exercise_response(actual: UpdateExerciseRequestSchema, expected: UpdateExerciseResponseSchema):
    """
        Проверяет, что ответ на обновление данных задания соответствует ожидаемым данным.

        :param actual: Фактический ответ API
        :param expected: Ожидаемые данные задания
        :raises AssertionError: Если хотя бы одно поле не совпадает
        """
    logger.info("Check update exercise response")

    assert_equal(actual.title, expected.exercise.title, "title")
    assert_equal(actual.max_score, expected.exercise.max_score, "max_score")
    assert_equal(actual.min_score, expected.exercise.min_score, "min_score")
    assert_equal(actual.order_index, expected.exercise.order_index, "order_index")
    assert_equal(actual.description, expected.exercise.description, "description")
    assert_equal(actual.estimated_time, expected.exercise.estimated_time, "estimated_time")

@allure.step("Check exercise not found response")  # Добавили allure шаг
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если файл не найден на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "File not found"
    """
    logger.info("Check exercise not found response")

    # Ожидаемое сообщение об ошибке, если файл не найден
    expected = InternalErrorResponseSchema(details="Exercise not found")
    # Используем ранее созданную функцию для проверки внутренней ошибки
    assert_internal_error_response(actual, expected)

@allure.step("Check get exercises response")  # Добавили allure шаг
def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        create_exercise_responses: list[CreateExerciseResponseSchema]
):
    """
    Проверяет, что ответ на получение списка заданий соответствует ответам на их создание.

    :param get_exercises_response: Ответ API при запросе списка заданий.
    :param create_exercise_responses: Список API ответов при создании заданий.
    :raises AssertionError: Если данные заданий не совпадают.
    """
    logger.info("Check get exercises response")

    assert_length(get_exercises_response.exercises, create_exercise_responses, "exercises")

    for index, create_exercise_response in enumerate(create_exercise_responses):
        assert_exercise(get_exercises_response.exercises[index], create_exercise_response.exercise)
