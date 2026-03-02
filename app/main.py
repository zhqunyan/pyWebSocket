from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

app = FastAPI()
_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(_dir, "templates"))

@app.get("/", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse("mysocket.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()

            # 消息处理
            if data == "__ping__":
                await websocket.send_text("__pong__")
            else:
                await websocket.send_text(f"服务端收到: {data}")

    except WebSocketDisconnect:
        print("客户端断开连接")
    except Exception as e:
        print(f"发生异常: {e}")
        # 记得主动关闭连接
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
    # uvicorn.run(app="main:app", reload=True, host="127.0.0.1", port=8080)