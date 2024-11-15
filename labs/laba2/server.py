import socketio
from aiohttp import web

# Создаем сервер Socket.IO
sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# Хранилище подключенных клиентов
connected_clients = {}


@sio.event
async def connect(sid, environ):
    print(f'Клиент подключился: {sid}')
    connected_clients[sid] = {}
    await sio.emit('message', {'msg': f'Клиент {sid} подключился!'})


@sio.event
async def disconnect(sid):
    print(f'Клиент отключился: {sid}')
    connected_clients.pop(sid, None)


@sio.event
async def chat_message(sid, data):
    print(f"Сообщение от {sid}: {data['msg']}")
    # Переслать сообщение всем клиентам
    await sio.emit('message', {'msg': f"{sid}: {data['msg']}"}, skip_sid=sid)


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
