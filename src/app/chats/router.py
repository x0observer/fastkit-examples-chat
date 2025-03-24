from typing import Type
from src.fastkit.routers.base import BaseRouter
from src.app.chats.models.chat import Chat, Message
from src.app.chats.schemas.chat import ChatCreate, ChatRead, MessageCreate, MessageRead
from src.app.chats.service import ChatService, MessageService


class MessageRouter(BaseRouter[Message, MessageCreate, MessageRead]):
    """Router for handling message operations."""

    def __init__(self, service_cls: Type[MessageService], prefix: str):
        super().__init__(service_cls, prefix, MessageCreate, MessageRead)


class ChatRouter(BaseRouter[Chat, ChatCreate, ChatRead]):
    """Router for handling chats operations."""

    def __init__(self, service_cls: Type[ChatService], prefix: str):
        super().__init__(service_cls, prefix, ChatCreate, ChatRead)