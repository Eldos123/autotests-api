import allure  # Импортируем allure
from httpx import Response

from clients.api_client import APIClient
from clients.exercises.exercises_schema import (
    GetExercisesQuerySchema,
    GetExercisesResponseSchema,
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema,
    GetExerciseQuerySchema,
    GetExerciseResponseSchema
)
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from tools.routes import APIRoutes  # Импортируем enum APIRoutes


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises
    """
    @allure.step("Get exercises")  # Добавили allure шаг
    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Метод получения списка заданий для определенного курса.
        :param query: Модель запроса с courseId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(APIRoutes.EXERCISES, params=query.model_dump(by_alias=True))

    @allure.step("Get exercise")  # Добавили allure шаг
    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод получения информации о задании по exercise_id.
        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.EXERCISES}/{exercise_id}")

    @allure.step("Create exercise")  # Добавили allure шаг
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """
        Метод создания задания.
        :param request: Модель запроса с title, courseId, maxScore, minScore, orderIndex, description,
        estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.EXERCISES, json=request.model_dump(by_alias=True))

    @allure.step("Update exercise")  # Добавили allure шаг
    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        """
        Метод обновления задания.
        :param exercise_id: Идентификатор задания.
        :param request: Модель запроса с title, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f"{APIRoutes.EXERCISES}/{exercise_id}", json=request.model_dump(by_alias=True))

    @allure.step("Delete exercise")  # Добавили allure шаг
    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод удаления задания.
        :param exercise_id: Идентификатор задания.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"{APIRoutes.EXERCISES}/{exercise_id}")

    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        """
        Метод получения списка заданий для определенного курса с валидацией ответа.
        :param query: Модель запроса с courseId.
        :return: Валидированная модель ответа получения списка заданий.
        :raises ValidationError: Если ответ сервера не соответствует схеме.
        """
        response = self.get_exercises_api(query)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def get_exercise(self, query: GetExerciseQuerySchema) -> GetExerciseResponseSchema:
        """
        Метод получения информации о задании по exercise_id с валидацией ответа.
        :param query: Модель запроса с exerciseId.
        :return: Валидированная модель ответа получения задания.
        :raises ValidationError: Если ответ сервера не соответствует схеме.
        """
        response = self.get_exercise_api(query.model_dump(by_alias=True)["id"])
        response.raise_for_status()  # Проверка на ошибки HTTP
        return GetExerciseResponseSchema.model_validate_json(response.text)

    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        """
        Метод создания задания с валидацией ответа.
        :param request: Модель запроса с title, courseId, maxScore, minScore, orderIndex, description,
        estimatedTime.
        :return: Валидированная модель ответа создания задания.
        :raises ValidationError: Если ответ сервера не соответствует схеме.
        """
        response = self.create_exercise_api(request)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> UpdateExerciseResponseSchema:
        """
        Метод обновления задания с валидацией ответа.
        :param exercise_id: Идентификатор задания.
        :param request: Модель запроса с title, maxScore, minScore, orderIndex, description, estimatedTime.
        :return: Валидированная модель ответа обновления задания.
        :raises ValidationError: Если ответ сервера не соответствует схеме.
        """
        response = self.update_exercise_api(exercise_id, request)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return UpdateExerciseResponseSchema.model_validate_json(response.text)

    def delete_exercise(self, exercise_id: str) -> dict:
        """
        Метод удаления задания с возвратом JSON-ответа.
        :param exercise_id: Идентификатор задания.
        :return: Распарсенный JSON-ответ от сервера.
        :raises HTTPStatusError: Если сервер вернул ошибку.
        """
        response = self.delete_exercise_api(exercise_id)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()

def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.
    :param user: Данные пользователя для аутентификации.
    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))