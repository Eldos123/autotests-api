import uuid
from pydantic import BaseModel, Field, EmailStr, ValidationError


# модель данных пользователя
class UserSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr  # Используем EmailStr вместо str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

# запрос на создание пользователя
class CreateUserRequestSchema(BaseModel):
    email: EmailStr # Используем EmailStr вместо str
    password: str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

# ответ с данными созданного пользователя
class CreateUserResponseSchema(BaseModel):
    user: UserSchema

# Инициализируем модель CreateUserRequestSchema через передачу аргументов
user_default_model = CreateUserRequestSchema(
    email="user@example.com",
    password="StrongPass123!",
    lastName="Doe",
    firstName="John",
    middleName="Middle"
)
print('User default model:', user_default_model)

# Инициализируем модель CreateUserRequestSchema через распаковку словаря
user_dict = {
    "email": "user@example.com",
    "password": "StrongPass123!",
    "lastName": "Doe",
    "firstName": "John",
    "middleName": "Middle"
}
user_dict_model = CreateUserRequestSchema(**user_dict)
print('User dict model:', user_dict_model)
print(user_dict_model.model_dump())
print(user_dict_model.model_dump(by_alias=True))

# Инициализируем модель CreateUserRequestSchema через JSON
user_json = """
{
    "email": "user@example.com",
    "password": "StrongPass123!",
    "lastName": "Doe",
    "firstName": "John",
    "middleName": "Middle"
}
"""
user_json_model = CreateUserRequestSchema.model_validate_json(user_json)
print('User JSON model:', user_json_model)

# Инициализируем CreateUserRequestSchema c некорректным email
try:
    user = CreateUserRequestSchema(
        email="examplecom",
        password="StrongPass123!",
        lastName="Doe",
        firstName="John",
        middleName="Middle"
    )
except ValidationError as error:
    print(error)
    print(error.errors())
