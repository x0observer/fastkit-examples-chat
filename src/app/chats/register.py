
from src.app.chats.service import ChatService, MessageService
from src.app.chats.router import ChatRouter, MessageRouter
from src.middleware.engine import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
# ...

def get_chat_service(db_session: AsyncSession = Depends(get_async_session)) -> ChatService:
    return ChatService(db_session)

chat_router = ChatRouter(service_cls=ChatService, prefix="/chats").get_router()


def get_message_service(db_session: AsyncSession = Depends(get_async_session)) -> MessageService:
    return MessageService(db_session)

message_router = MessageRouter(service_cls=MessageService, prefix="/messages").get_router()