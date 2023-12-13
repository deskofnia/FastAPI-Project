import uuid
from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from utils.websockets import manager


chat_html = """<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>ChatApp</title>
                <!-- Latest compiled and minified CSS -->
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                <!-- jQuery library -->
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <style>
                    .card {
                        position: absolute;
                        width: 95%;
                        height: 80%;
                        box-shadow: 0px 0px 5px gray;
                        left: 2.5%;
                        top: 5%;
                    }
                    #chat-form {
                        position: absolute;
                        top: 90%;
                        transform: translateY(-90%);
                        left: 50%;
                        transform: translateX(-50%);
                    }
                    #messages {
                        padding-bottom: 10%;
                        padding-left: 20px;
                        padding-top: 20px;
                        max-height: 80%;
                        overflow: auto;
                    }
                    #chat-form input {
                        width: 400px;
                        padding-right: 20%;
                    }
                    #chat-form button {
                        position: absolute;
                        left: 85%;
                    }
                    #profile {
                        position: absolute;
                        top: 20px;
                        left: 20px;
                    }
                </style>
                <script>
                    $(document).ready(function(){
                        var current_user;
                        $.get("/api/v1/message/current_user",function(response){
                            current_user = response;
                            $("#profile").text(current_user);
                        });
                        var receiver = "";
                        // create websocket
                        var socket = new WebSocket("ws://127.0.0.1:8000/api/v1/message/ws");
                        socket.onmessage = function(event) {
                            var parent = $("#messages");
                            var data = JSON.parse(event.data);
                            var sender = data['sender'];
                            if (sender == current_user)
                                sender = "You";
                            var message = data['message']
                            var content = "<p><strong>"+sender+" </strong> <span> "+message+"</span></p>";
                            parent.append(content);
                        };
                        $("#chat-form").on("submit", function(e){
                            e.preventDefault();
                            var message = $("input").val();
                            if (message){
                                data = {
                                    "sender": current_user,
                                    "message": message
                                };
                                socket.send(JSON.stringify(data));
                                $("input").val("");
                                document.cookie = 'X-Authorization=; path=/;';
                            }
                        });
                    });
                </script>
            </head>
            <body>
                <div class="chat-body card">
                    <div class="card-body">
                        <strong id="profile"></strong><h4 class="card-title text-center"> Chat App </h4>
                        <hr>
                        <div id="messages">
                        </div>
                        <form class="form-inline" id="chat-form">
                            <input type="text" class="form-control" placeholder="Write your message">
                            <button id="send" type="submit" class="btn btn-primary">Send</button>
                        </form>
                    </div>
                </div>
            </body>
            </html>"""

home_html = """ 
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ChatApp</title>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <style>
        .card {
            position: absolute;
            width: 95%;
            height: 80%;
            box-shadow: 0px 0px 5px gray;
            left: 2.5%;
            top: 5%;
        }
        #user-form {
            position: absolute;
            top: 20%;
            left: 50%;
            transform: translateX(-50%);
        }
        #user-form input {
            width: 400px;
            padding-right: 30%;
        }
        #user-form button {
            position: absolute;
            left: 75%;
            margin-left: 2px;
        }
    </style>
</head>
<script>
        $(document).ready(function(){
            $("#user-form").on("submit", function(e){
                e.preventDefault();
                var current_user = $("#user_input").val();
                if (current_user){
                    data = {"username": current_user};
                    $.post('/api/v1/message/register', JSON.stringify(data), function(response){
                        $(".chat-body").removeClass("hide");
                        $(".chat-register").addClass("hide");
                        window.location.href = "/api/v1/message/chat";
                    });
                }
            });
        });
    </script>
<body>
    <div class="chat-body card">
        <div class="card-body">
            <h4 class="card-title text-center"> Chat App </h4>
            <hr>
            <form class="form-inline" id="user-form">
                <input type="text" class="form-control" id="user_input" placeholder="Enter your name">
                <button id="start" type="submit" class="btn btn-primary">Start Chat</button>
            </form>
        </div>
    </div>
</body>
</html>"""

async def get_chat_html():
    return HTMLResponse(chat_html)

async def get_home_html():
    return HTMLResponse(home_html)

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
            await manager.send_personal_message(data, websocket)
            # await manager.broadcast(f"Client #{sender} says: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{sender} left the chat")
        # response = {
        #     "message": "left the chat"
        # }
        # await manager.send_personal_message(response)
   