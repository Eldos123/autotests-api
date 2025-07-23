import allure  # Импортируем allure
from httpx import Response

from clients.api_client import APIClient
from clients.api_coverage import tracker  # Импортируем трекер
from clients.courses.courses_schema import (
    GetCoursesQuerySchema,
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema,
    GetCourseQuerySchema,
    GetCourseResponseSchema
)
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from tools.routes import APIRoutes  # Импортируем enum APIRoutes


class CoursesClient(APIClient):
    """
    Клиент для работы с /api/v1/courses
    """

    @allure.step("Get courses")
    @tracker.track_coverage_httpx(APIRoutes.COURSES)
    def get_courses_api(self, query: GetCoursesQuerySchema) -> Response:
        """
        Метод получения списка курсов.
        :param query: Модель запроса с userId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(APIRoutes.COURSES, params=query.model_dump(by_alias=True))

    @allure.step("Get course by id {course_id}")
    @tracker.track_coverage_httpx(f"{APIRoutes.COURSES}/{{course_id}}")
    def get_course_api(self, course_id: str) -> Response:
        """
        Метод получения курса.
        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.COURSES}/{course_id}")

    @allure.step("Create course")
    @tracker.track_coverage_httpx(APIRoutes.COURSES)
    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        """
        Метод создания курса.
        :param request: Модель запроса с title, maxScore, minScore, description,
        estimatedTime, previewFileId, createdByUserId.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(APIRoutes.COURSES, json=request.model_dump(by_alias=True))

    @allure.step("Update course by id {course_id}")  # Добавили allure шаг
    @tracker.track_coverage_httpx(f"{APIRoutes.COURSES}/{{course_id}}")
    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        """
        Метод обновления курса.
        :param course_id: Идентификатор курса.
        :param request: Модель запроса с title, maxScore, minScore, description, estimatedTime.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(
            f"{APIRoutes.COURSES}/{course_id}",
            json=request.model_dump(by_alias=True)
        )

    @allure.step("Delete course by id {course_id}")  # Добавили allure шаг
    @tracker.track_coverage_httpx(f"{APIRoutes.COURSES}/{{course_id}}")
    def delete_course_api(self, course_id: str) -> Response:
        """
        Метод удаления курса.
        :param course_id: Идентификатор курса.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"{APIRoutes.COURSES}/{course_id}")

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        """
        Метод создания курса с валидацией ответа.
        :param request: Модель запроса с title, maxScore, minScore, description,
        estimatedTime, previewFileId, createdByUserId.
        :return: Валидированная модель ответа создания курса.
        :raises ValidationError: Если ответ сервера не соответствует схеме.
        """
        response = self.create_course_api(request)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return CreateCourseResponseSchema.model_validate_json(response.text)

    def get_course(self, query: GetCourseQuerySchema) -> GetCourseResponseSchema:
        """
        Метод получения курса с валидацией ответа.
        :param query: Модель запроса с courseId.
        :return: Валидированная модель ответа получения курса.
        :raises ValidationError: Если ответ сервера не соответствует схеме.
        """
        response = self.get_course_api(query.model_dump(by_alias=True)["id"])
        response.raise_for_status()  # Проверка на ошибки HTTP
        return GetCourseResponseSchema.model_validate_json(response.text)

    def update_course(self, course_id: str, request: UpdateCourseRequestSchema) -> UpdateCourseResponseSchema:
        """
        Метод обновления курса с валидацией ответа.
        :param course_id: Идентификатор курса.
        :param request: Модель запроса с title, maxScore, minScore, description, estimatedTime.
        :return: Валидированная модель ответа обновления курса.
        :raises ValidationError: Если ответ сервера не соответствует схеме.
        """
        response = self.update_course_api(course_id, request)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return UpdateCourseResponseSchema.model_validate_json(response.text)


def get_courses_client(user: AuthenticationUserSchema) -> CoursesClient:
    """
    Функция создаёт экземпляр CoursesClient с уже настроенным HTTP-клиентом.
    :return: Готовый к использованию CoursesClient.
    """
    return CoursesClient(client=get_private_http_client(user))