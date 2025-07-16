import pytest
from pydantic import BaseModel

from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.users import UserFixture

@pytest.fixture(scope="function")
class ExerciseFixture(BaseModel):
    """
    Модель для хранения данных запроса и ответа на создание задания.
    """
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema

def exercises_client(function_user: UserFixture) -> ExercisesClient:
    """
    Фикстура для создания экземпляра API-клиента ExercisesClient.

    :param function_user: Фикстура пользователя, содержащая данные аутентификации.
    :return: Экземпляр ExercisesClient.
    """
    return get_exercises_client(function_user.authentication_user)

def function_exercise(
        exercises_client: ExercisesClient,
        function_user: UserFixture,
        function_course: CourseFixture
) -> ExerciseFixture:
    """
    Фикстура для создания тестового задания.

    :param exercises_client: Фикстура клиента для работы с API заданий.
    :param function_user: Фикстура пользователя, содержащая данные пользователя.
    :param function_course: Фикстура курса, содержащая данные курса.
    :return: Объект ExerciseFixture с данными запроса и ответа.
    """
    request = CreateExerciseRequestSchema(
        course_id=function_course.response.course.id,
        created_by_user_id=function_user.response.user.id
    )
    response = exercises_client.create_exercise(request)
    return ExerciseFixture(request=request, response=response)