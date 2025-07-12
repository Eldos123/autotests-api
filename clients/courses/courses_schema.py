from pydantic import BaseModel, Field, ConfigDict
from ..users.users_schema import UserSchema
from ..files.files_schema import FileSchema

# Модель курса
class Course(BaseModel):
    """
    Описание структуры курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    description: str
    preview_file: FileSchema = Field(alias="previewFile")
    estimated_time: str = Field(alias="estimatedTime")
    created_by_user: UserSchema = Field(alias="createdByUser")

# Запрос на получение списка курсов
class GetCoursesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка курсов.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")

# Запрос на создание курса
class CreateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    description: str
    estimated_time: str = Field(alias="estimatedTime")
    preview_file_id: str = Field(alias="previewFileId")
    created_by_user_id: str = Field(alias="createdByUserId")

# Ответ на создание курса
class CreateCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    course: Course

# Запрос на обновление курса
class UpdateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(alias="title")
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    description: str | None = Field(alias="description")
    estimated_time: str | None = Field(alias="estimatedTime")

# Ответ на обновление курса
class UpdateCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    course: Course

# Запрос на получение одного курса
class GetCourseQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение одного курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias="id")

# Ответ на получение одного курса
class GetCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа получения одного курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    course: Course