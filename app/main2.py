
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import socketio

# 创建Socket.IO异步服务器实例
sio = socketio.AsyncServer(async_mode='asgi')
app = FastAPI()

# 将Socket.IO挂载进FastAPI应用
combined_app = socketio.ASGIApp(sio, other_asgi_app=app)


@app.get("/", response_class=HTMLResponse)
async def index():
    import os
    _dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(_dir, "templates/socketio.html"), encoding='utf-8') as f:
        html_content = f.read()
    return HTMLResponse(html_content)


@sio.event
async def connect(sid, environ):
    print(f"[{sid}] 用户建立连接")
    await sio.emit('broadcast_message', {'message': f"{sid[:6]} 加入房间"}, room=None)


@sio.event
async def disconnect(sid):
    print(f"[{sid}] 用户断开连接")


@sio.event
async def send_message(sid, data):
    user_msg = data['message']
    full_msg = f"<strong>{sid[:6]}</strong>: {user_msg}"
    print(full_msg)
    await sio.emit('broadcast_message', {'message': full_msg})

if __name__ == '__main__':
    try:
        config = uvicorn.Config(
            combined_app, host="127.0.0.1", port=8000, log_level="info")
        server = uvicorn.Server(config)
        server.run()
    except KeyboardInterrupt:
        pass
