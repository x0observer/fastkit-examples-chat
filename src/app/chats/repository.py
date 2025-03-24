
from sqlalchemy.ext.asyncio import AsyncSession
from src.fastkit.repositories.base import BaseRepository
from src.app.chats.models.chat import (Chat, ChatParticipant, Message)


class ChatRepository(BaseRepository[Chat]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Chat, db_session)


class MessageRepository(BaseRepository[Message]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Chat, db_session)