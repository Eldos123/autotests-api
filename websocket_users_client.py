import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = "Привет, сервер!"
        print(f"Отправка: {message}")
        await websocket.send(message)

        # Получаем ровно пять ответов от сервера
        for i in range(5):
            response = await websocket.recv()
            print(f"{i+1} {response}")

asyncio.run(client())