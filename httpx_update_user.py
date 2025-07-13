import httpx

from tools.fakers import fake.email

# Создаем пользователя
create_user_payload = {
    "email": fake.email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}
create_user_response = httpx.post("http://localhost:8000/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()
print(create_user_response.status_code)
print('Create user data:', create_user_response_data)


# Проходим аутентификацию
login_payload = {
    "email": create_user_payload['email'],
    "password": create_user_payload['password']
}
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print(login_response.status_code)
print('Login data:', login_response_data)

# Новые данные пользователя
patch_user_payload = {
    "email": fake.email(),
    "password": "update_string",
    "lastName": "update_string",
    "firstName": "update_string",
    "middleName": "update_string"
}

user_headers = {
    "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
}
patch_user_response = httpx.patch(
    f"http://localhost:8000/api/v1/users/{create_user_response_data['user']['id']}",
    json=patch_user_payload, headers=user_headers
)
patch_user_response_data = patch_user_response.json()
print(patch_user_response.status_code)
print('patch user data:', patch_user_response_data)
