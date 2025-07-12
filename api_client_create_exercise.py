from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.fakers import get_random_email

# Инициализация клиента для публичных пользователей
public_users_client = get_public_users_client()

# Создание пользователя
create_user_request = CreateUserRequestSchema(
    email=get_random_email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
create_user_response = public_users_client.create_user(create_user_request)
print('Create user data:', create_user_response.model_dump(by_alias=True))

# Инициализация клиентов с аутентификацией
authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercises_client = get_exercises_client(authentication_user)

# Загрузка файла
create_file_request = CreateFileRequestSchema(
    filename="image.png",
    directory="exercises",
    upload_file="./testdata/files/image.png"
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response.model_dump(by_alias=True))

# Создание курса
create_course_request = CreateCourseRequestSchema(
    title="Python для начинающих",
    max_score=100,
    min_score=10,
    description="Курс по основам Python",
    estimated_time="2 недели",
    preview_file_id=create_file_response.file.id,
    created_by_user_id=create_user_response.user.id
)
create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response.model_dump(by_alias=True))

# Создание задания
create_exercise_request = CreateExerciseRequestSchema(
    title="Первое задание по Python",
    course_id=create_course_response.course.id,
    max_score=50,
    min_score=0,
    order_index=1,
    description="Напишите простую программу на Python",
    estimated_time="1 час"
)
create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print('Create exercise data:', create_exercise_response.model_dump(by_alias=True))