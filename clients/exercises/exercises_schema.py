from pydantic import BaseModel, Field, ConfigDict
from typing import List
from tools.fakers import fake

# Модель задания
class ExerciseSchema(BaseModel):
    """
    Описание структуры задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")

# Запрос на получение списка заданий
class GetExercisesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка заданий для определенного курса.
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias="courseId")

# Ответ на получение списка заданий
class GetExercisesResponseSchema(BaseModel):
    """
    Описание структуры ответа получения списка заданий.
    """
    model_config = ConfigDict(populate_by_name=True)

    exercises: List[ExerciseSchema] = Field(default_factory=list, alias="exercises")

# Запрос на создание задания
class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    course_id: str = Field(alias="courseId", default_factory=fake.uuid4)
    max_score: int = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int = Field(alias="minScore", default_factory=fake.min_score)
    order_index: int = Field(alias="orderIndex", default_factory=fake.integer)
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(alias="estimatedTime", default_factory=fake.estimated_time)

# Ответ на создание задания
class CreateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    exercise: ExerciseSchema

# Запрос на обновление задания
class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление данных задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(alias="title", default_factory=fake.sentence)
    max_score: int | None = Field(alias="maxScore", default_factory=fake.max_score)
    min_score: int | None = Field(alias="minScore", default_factory=fake.min_score)
    order_index: int | None = Field(alias="orderIndex", default_factory=fake.integer)
    description: str | None = Field(alias="description", default_factory=fake.text)
    estimated_time: str | None = Field(alias="estimatedTime", default_factory=fake.estimated_time)

# Ответ на обновление задания
class UpdateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    exercise: ExerciseSchema

# Запрос на получение одного задания
class GetExerciseQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение одного задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    exercise_id: str = Field(alias="id")

# Ответ на получение одного задания
class GetExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа получения одного задания.
    """
    model_config = ConfigDict(populate_by_name=True)

    exercise: ExerciseSchema