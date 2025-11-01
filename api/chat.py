from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect

chat_client_html = """
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
            var ws = new WebSocket("ws://localhost:8001/chat/ws");
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

router = APIRouter(
    tags=["chat"],
    prefix="/chat"
)

@router.get("/client")
def get_chat_client():
    return HTMLResponse(chat_client_html)

# websocket_clients:list[WebSocket] = []
@router.websocket("/ws")
async def websocket_enpoint(websocket: WebSocket):
    await websocket.accept() # Accept the incoming WebSocket connection
    # websocket_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text() # Receive data from the client
            await websocket.send_text(f"Your message was: {data}") # Send data back to the client
            # print(f"Totle {len(websocket_clients)} websocket_clients")
            # for client in websocket_clients:
            #     await client.send_text(f"Message was: {data}") # Send data back to ALL clients
    except WebSocketDisconnect:
        print(f"Client disconnected")