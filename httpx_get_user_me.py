import httpx  # Импортируем библиотеку HTTPX

# Данные для входа в систему
login_payload = {
    "email": "user@example.com",
    "password": "string"
}

# Выполняем запрос на аутентификацию
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

# Выводим полученные токены
print("Login response:", login_response_data)
print("Status Code:", login_response.status_code)

# Формируем payload для GET-запроса
token = login_response_data["token"]["accessToken"]
headers = {"Authorization": f"Bearer {token}"}

# Выполняем GET-запроса
me_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=headers)
me_response_data = me_response.json()

# Выводим данные GET-запроса
print("GET response:", me_response_data)
print("Status Code:", me_response.status_code)