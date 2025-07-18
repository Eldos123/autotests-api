import pytest
from http import HTTPStatus

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseResponseSchema, UpdateExerciseRequestSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_exercise, \
    assert_update_exercise_response, assert_exercise_not_found_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(self, exercises_client: ExercisesClient, function_course: CourseFixture):
        """
        Тест проверяет создание задания через API.

        :param exercises_client: Экземпляр ExercisesClient для выполнения API-запросов
        :param function_course: Фикстура, предоставляющая данные курса
        :raises AssertionError: Если код ответа, тело ответа или JSON-схема не соответствуют ожидаемым
        """
        # Формируем данные для создания задания, используя схему CreateExerciseRequestSchema
        request = CreateExerciseRequestSchema(
            course_id=function_course.response.course.id,
        )

        # Отправляем запрос на создание задания
        response = exercises_client.create_exercise_api(request)

        # Преобразуем JSON-ответ в объект схемы CreateExerciseResponseSchema
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверяем, что данные в ответе соответствуют запросу
        assert_create_exercise_response(request, response_data)

    def test_get_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        """
        Тест проверяет получение задания через API.

        :param exercises_client: Экземпляр ExercisesClient для выполнения API-запросов
        :param function_exercise: Фикстура, предоставляющая данные задания
        :raises AssertionError: Если код ответа, тело ответа или JSON-схема не соответствуют ожидаемым
        """
        # Отправляем GET-запрос на получение задания
        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)

        # Десериализуем JSON-ответ в Pydantic-модель
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверяем, что данные задания соответствуют ожидаемым
        assert_exercise(response_data.exercise, function_exercise.response.exercise)

        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        # Формируем данные для обновления
        request = UpdateExerciseRequestSchema()
        # Отправляем запрос на обновление курса
        response = exercises_client.update_exercise_api(function_exercise.response.exercise.id, request)
        # Преобразуем JSON-ответ в объект схемы
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_update_exercise_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())


    def test_delete_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        """
        Тест проверяет удаление задания и последующую попытку его получения.
        """
        # 1. Удаляем файл
        delete_response = exercises_client.delete_exercise_api(function_exercise.response.exercise.id)
        # 2. Проверяем, что файл успешно удален (статус 200 OK)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # 3. Пытаемся получить удаленное задание
        # отправляем GET-запрос на получение задания
        get_response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        # 4. Проверяем, что сервер вернул 404 Not Found
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        # 5. Проверяем, что в ответе содержится ошибка "File not found"
        assert_exercise_not_found_response(get_response_data)

        # 6. Проверяем, что ответ соответствует схеме
        validate_json_schema(get_response.json(), get_response_data.model_json_schema())
