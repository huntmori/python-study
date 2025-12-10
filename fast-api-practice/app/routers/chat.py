import json

from fastapi import FastAPI, WebSocket, APIRouter
from starlette.websockets import WebSocketDisconnect

import logging

from app.Classes.ConnectionManager import ConnectionManager

router = APIRouter(prefix="/ws/chat", tags=["Chat"])

manager = ConnectionManager()

logger = logging.getLogger(__name__)

@router.websocket(path='', name='Chat')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            text = await websocket.receive_text()
            data = json.loads(text)

            type: str = data.get("type")

            logger.info(f"Received message of type {type}")

            if type == "ws_headers":
                # Handle different message types here
                await manager.send_personal_message(text,websocket)
            else:
                await manager.send_personal_message(text,websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{websocket.client.host} left the chat")