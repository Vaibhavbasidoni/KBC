from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import json
import random
import qrcode
import base64
from io import BytesIO
from fastapi.responses import FileResponse
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sample questions
questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "Which planet is known as the Red Planet?", "answer": "Mars"},
    {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"},
    {"question": "What is the largest mammal in the world?", "answer": "Blue Whale"},
    {"question": "In which year did World War II end?", "answer": "1945"}
]

current_question = 0
players = {}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global current_question
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received message: {data}")
            message = json.loads(data)
            if message["type"] == "join":
                players[websocket] = message["name"]
                logger.info(f"Player joined: {message['name']}")
                await websocket.send_text(json.dumps({"type": "question", "question": questions[current_question]["question"]}))
            elif message["type"] == "answer":
                logger.info(f"Answer received: {message['answer']}")
                if message["answer"].lower() == questions[current_question]["answer"].lower():
                    logger.info("Correct answer")
                    await manager.broadcast(json.dumps({
                        "type": "correct_answer",
                        "player": players[websocket],
                        "question": questions[current_question]["question"]
                    }))
                    current_question = (current_question + 1) % len(questions)
                    await asyncio.sleep(3)  # Wait for 3 seconds
                    qr_code = generate_qr_code(f"http://localhost:8002/static/player.html")
                    await manager.broadcast(json.dumps({
                        "type": "new_question",
                        "question": questions[current_question]["question"],
                        "qr_code": qr_code
                    }))
                else:
                    logger.info("Wrong answer")
                    await websocket.send_text(json.dumps({"type": "wrong_answer"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        del players[websocket]
        logger.info("WebSocket disconnected")

@app.get("/")
async def get():
    global current_question
    current_question = 0
    qr_code = generate_qr_code(f"http://localhost:8001/static/player.html")
    return {
        "question": questions[current_question]["question"],
        "qr_code": qr_code
    }

@app.get("/host")
async def host():
    return FileResponse("static/host.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
