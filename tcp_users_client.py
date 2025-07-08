import socket


def send_message(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)

    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    print(f"Ответ сервера: {response}")
    client_socket.close()


if __name__ == '__main__':
    # Первый клиент (отправляет только "Привет, сервер!")
    print("Клиент 1 отправляет: Привет, сервер!")
    send_message("Привет, сервер!")

    # Второй клиент (отправляет только "Как дела?")
    print("\nКлиент 2 отправляет: Как дела?")
    send_message("Как дела?")