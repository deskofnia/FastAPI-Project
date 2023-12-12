import uuid
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from utils.websockets import manager


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/api/v1/message/chat");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

async def get_html():
    return HTMLResponse(html)

async def token_generator(name: str, request):

    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc": "name",  "msg": "Enter a valid name"})

    token = str(uuid.uuid4())

    data = {"name": name, "token": token}

    return data

async def websocket_endpoint(websocket: WebSocket):
    sender = websocket.cookies.get("X-Authorization")

    if sender:
        await manager.connect(websocket, sender)
        response = {
            "sender": sender,
            "message": "connected to websocket"
        }
        await manager.broadcast(response)
        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(data)

        except WebSocketDisconnect:
            manager.disconnect(websocket, sender)
            response = {
                "message": "left the chat"
            }
            await manager.broadcast(response)