
from src.app.auth.service import AuthService
from src.app.auth.router import AuthRouter
from src.middleware.engine import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
# ...

def get_auth_service(db_session: AsyncSession = Depends(get_async_session)) -> AuthService:
    """Возвращает экземпляр FileService с уже подключенной сессией."""
    return AuthService(db_session)

auth_router = AuthRouter(service_cls=AuthService, prefix="/me").get_router()