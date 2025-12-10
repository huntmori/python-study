import json
from typing import Dict, Optional
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket
import logging
from app.database import get_db
from app.auth import (
    decode_access_token,
)
from app.dtos import BaseResponse
from app.models import User

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        # 키는 사용자 식별자(uid 또는 id 또는 username)로 저장
        self.log_in_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        logger.info("websocket header : %s", websocket.headers)
        logger.info("websocket cookies : %s", websocket.cookies)
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, recipient: WebSocket):
        await recipient.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def logIn(self, websocket: WebSocket, token: Optional[str]):
        """
        websocket에서 호출할 때 DB 의존성 주입이 되지 않으므로 get_db() 제너레이터를 직접 사용합니다.
        token: 암호화된(전송된) 토큰 문자열
        """
        logger.info(f"logIn : token ={token}")

        if not token:
            await websocket.send_text(
                json.dumps(
                    BaseResponse.error("Invalid token")
                )
            )
            return

        # 토큰 복호화 및 사용자명 추출
        try:
            decoded = decode_access_token(token)
        except Exception as e:
            logger.exception("token decode failed")
            await websocket.send_text(
                json.dumps(
                    BaseResponse.error("Invalid token")
                )
            )
            return

        # decode_access_token이 문자열(예: username) 또는 dict(payload)를 반환할 수 있으므로 안전하게 처리
        user_name: Optional[str] = None
        if isinstance(decoded, str):
            user_name = decoded
        elif isinstance(decoded, dict):
            # 표준적으로 'sub' 또는 'username' 키 사용 가능성 처리
            user_name = decoded.get("sub") or decoded.get("username") or decoded.get("user")
        else:
            user_name = None

        logger.info(f"user_name : {user_name}")

        if not user_name:
            await websocket.send_text(
                json.dumps(
                    BaseResponse.error("Invalid token payload")
                )
            )
            return

        # get_db 제너레이터를 직접 사용하여 세션을 얻고, finally에서 정리
        db_gen = get_db()
        try:
            db = next(db_gen)
        except StopIteration:
            logger.error("Failed to obtain DB session from get_db()")
            await websocket.send_text(
                json.dumps(
                    BaseResponse.error("DB server error")
                )
            )
            return

        try:
            user = db.query(User).filter(User.username == user_name).first()
            if not user:
                logger.error("Invalid token or user not found")
                await websocket.send_text(
                    json.dumps(
                        BaseResponse.error("Invalid token or user not found")
                    )
                )
                return

            # 안전한 사용자 식별자 추출 (uid, id, username 순)
            uid = getattr(user, "uid", None) or getattr(user, "id", None) or getattr(user, "username", None)
            if uid is None:
                logger.error("User has no usable identifier")
                await websocket.send_text(
                    json.dumps(
                        BaseResponse.error("User has no usable identifier")
                    )
                )
                return

            # 로그인 연결 저장
            self.log_in_connections[str(uid)] = websocket

            # 직렬화 가능한 사용자 정보만 전송
            user_info = {
                "uid": uid,
                "username": getattr(user, "username", None),
                "email": getattr(user, "email", None),
                # 필요한 추가 필드만 담음
            }
            await websocket.send_text(
                json.dumps(
                    BaseResponse.success("", user_info)
                )
            )
        finally:
            # 제너레이터를 닫아 DB 세션 정리 코드 실행
            try:
                db_gen.close()
            except Exception:
                pass
