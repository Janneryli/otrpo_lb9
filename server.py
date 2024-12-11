import tornado.ioloop
import tornado.web
import tornado.websocket
import redis
import asyncio
import uuid
import random


class ChatWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = {}  # Словарь для хранения клиентов {WebSocketHandler: {"id": ID, "color": цвет}}

    def open(self):
        # Генерация уникального ID и цвета для каждого клиента
        unique_id = str(uuid.uuid4())
        color = self.generate_random_color()
        ChatWebSocketHandler.clients[self] = {"id": unique_id, "color": color}
        self.update_clients_list()
        print(f"Новый пользователь подлючился: {unique_id} with color {color}")

    def on_message(self, message):
        print(f"Отправленное сообщение: {message}")
        client_data = ChatWebSocketHandler.clients[self]
        data = {
            "type": "message",
            "content": message,
            "color": client_data["color"],  # Передаем цвет клиента
        }
        # Публикуем сообщение в Redis
        self.application.redis_client.publish("Чат", tornado.escape.json_encode(data))

    def on_close(self):
        # Удаляем клиента из списка
        if self in ChatWebSocketHandler.clients:
            del ChatWebSocketHandler.clients[self]
        self.update_clients_list()
        print("Пользователь отключился")

    def check_origin(self, origin):
        return True

    def update_clients_list(self):
        # Отправка списка уникальных клиентов
        clients_ids = [data["id"] for data in ChatWebSocketHandler.clients.values()]
        data = {
            "type": "clients",
            "clients": clients_ids,
        }
        for client in ChatWebSocketHandler.clients:
            client.write_message(tornado.escape.json_encode(data))

    @staticmethod
    def generate_random_color():
        return "#{:02x}{:02x}{:02x}".format(0, random.randint(100, 255), random.randint(200, 255))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


async def listen_to_redis(redis_client):
    pubsub = redis_client.pubsub()
    pubsub.subscribe("Чат")  # Подписываемся на канал "chat"
    print("Listening to Redis channel: chat")
    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            # Рассылаем сообщение всем клиентам
            for client in ChatWebSocketHandler.clients:
                client.write_message(message["data"].decode("utf-8"))
        await asyncio.sleep(0.1)  # Пауза для предотвращения блокировки


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", ChatWebSocketHandler),
    ])


if __name__ == "__main__":
    # Подключаемся к Redis
    redis_client = redis.Redis()

    # Создаем приложение Tornado
    app = make_app()
    app.redis_client = redis_client

    # Запускаем задачу для подписки на Redis через Tornado
    tornado.ioloop.IOLoop.current().spawn_callback(listen_to_redis, redis_client)

    # Запускаем Tornado
    app.listen(8888)
    print("Server started at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
