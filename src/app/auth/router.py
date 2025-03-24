from typing import Type
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from src.fastkit.routers.base import BaseRouter
from src.app.auth.models.user import User
from src.app.auth.schemas.user import UserCreate, UserRead, UserPublic, UserResponse
from src.app.auth.service import AuthService
from src.middleware.engine import AsyncSession, get_async_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="me/login")

class AuthRouter(BaseRouter[User, UserCreate, UserRead]):
    """Router for handling auth/user operations."""

    def __init__(self, service_cls: Type[AuthService], prefix: str):
        super().__init__(service_cls, prefix, UserCreate, UserRead)
        
        
        @self.router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Authorize: Public"]) 
        async def register(
            user_data: UserPublic = Depends(),
            db_session: AsyncSession = Depends(get_async_session),
        ):
            service = self.service_cls(db_session)
            db_user = await service.register(user_data)
            return UserResponse.model_validate(db_user, from_attributes=True)


        @self.router.post("/login", status_code=status.HTTP_201_CREATED, tags=["Authorize: Public"]) 
        async def login(
            form_data: OAuth2PasswordRequestForm = Depends(),
            db_session: AsyncSession = Depends(get_async_session),
        ):
            service = self.service_cls(db_session)
            return await service.login(form_data.username, form_data.password)
        

        @self.router.post("/protected", status_code=status.HTTP_201_CREATED, tags=["Authorize: Public"]) 
        async def protected(
            token: str = Depends(oauth2_scheme),
            db_session: AsyncSession = Depends(get_async_session),
        ):
            service = self.service_cls(db_session)
            return service.verify_token(token)