
from src.middleware.engine import AsyncSession
from src.fastkit.services.base import BaseService
from .repository import ChatRepository, MessageRepository
from .models.chat import Chat, Message
from src.fastkit.utils.serverless import serverless, serviceable, Provide


class MessageService(BaseService[Message]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        super().__init__(MessageRepository(db_session))

        
@serverless([MessageService])
class ChatService(BaseService[Chat]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        super().__init__(ChatRepository(db_session))