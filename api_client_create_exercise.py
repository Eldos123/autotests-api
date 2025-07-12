from clients.courses.courses_client import get_courses_client, CreateCourseRequestDict
from clients.exercises.exercises_client import get_exercises_client, CreateExerciseRequestDict
from clients.files.files_client import get_files_client, CreateFileRequestDict
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client, CreateUserRequestDict
from tools.fakers import get_random_email

# Инициализация клиента для публичных пользователей
public_users_client = get_public_users_client()

# Создание пользователя
create_user_request = CreateUserRequestDict(
    email=get_random_email(),
    password="string",
    lastName="string",
    firstName="string",
    middleName="string"
)
create_user_response = public_users_client.create_user(create_user_request)

# Инициализация клиентов с аутентификацией
authentication_user = AuthenticationUserSchema(
    email=create_user_request['email'],
    password=create_user_request['password']
)
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercises_client = get_exercises_client(authentication_user)

# Загрузка файла
create_file_request = CreateFileRequestDict(
    filename="image.png",
    directory="exercises",
    upload_file="./testdata/files/image.png"
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

# Создание курса
create_course_request = CreateCourseRequestDict(
    title="Python для начинающих",
    maxScore=100,
    minScore=10,
    description="Курс по основам Python",
    estimatedTime="2 недели",
    previewFileId=create_file_response['file']['id'],
    createdByUserId=create_user_response['user']['id']
)
create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response)

# Создание задания
create_exercise_request = CreateExerciseRequestDict(
    title="Первое задание по Python",
    courseId=create_course_response['course']['id'],
    maxScore=50,
    minScore=0,
    orderIndex=1,
    description="Напишите простую программу на Python",
    estimatedTime="1 час"
)
create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print('Create exercise data:', create_exercise_response)
