import uuid
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from utils.websockets import manager



async def token_generator(name: str, request):

    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc": "name",  "msg": "Enter a valid name"})

    token = str(uuid.uuid4())

    data = {"name": name, "token": token}

    return data

async def websocket_endpoint(websocket: WebSocket):
    sender = websocket.cookies.get("X-Authorization")

    await manager.connect(websocket)
    # response = {
    #     "sender": sender,
    #     "message": "connected to websocket"
    # }
    # await manager.broadcast(response)
    try:
        while True:
            data = await websocket.receive_text()
            # user, msg = (data)
            # await manager.send_personal_message(data, websocket)
            await manager.broadcast(data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{sender} left the chat")
        # response = {
        #     "message": "left the chat"
        # }
        # await manager.send_personal_message(response)
   