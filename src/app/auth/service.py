from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from src.middleware.engine import AsyncSession
from src.fastkit.services.base import BaseService
from src.app.auth.schemas.user import UserPublic
from .repository import AuthRepository
from .models.user import User
from setup import (AUTH_ACCESS_TOKEN_EXPIRE_MINUTES, AUTH_ALGORITHM, AUTH_SECRET_KEY)
from jose import JWTError, jwt

class AuthService(BaseService[User]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        super().__init__(AuthRepository(db_session))
        

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT token with the provided data and expiration time.

        Args:
            data (dict): Data to include in the token (e.g., user_id).
            expires_delta (Optional[timedelta]): Lifetime of the token.

        Returns:
            str: Encoded JWT token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=int(AUTH_ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str) -> Optional[dict]:
        """
        Decode a JWT token and return its payload.

        Args:
            token (str): JWT token to decode.

        Returns:
            Optional[dict]: Decoded payload or None if the token is invalid.
        """
        try:
            payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
            return payload
        except JWTError:
            return None


    def verify_token(self, token: str) -> dict:
        """
        Verify the JWT token and return its payload.

        Args:
            token (str): The JWT token.

        Returns:
            dict: The decoded payload.

        Raises:
            HTTPException: If the token is invalid.
        """
        payload = self.decode_access_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload


    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.

        Args:
            username (str): The username.
            password (str): The password.

        Returns:
            Optional[User]: User object if authentication is successful, otherwise None.
        """
        user = await self.repository.get_by_username(username)
        if not user or not user.verify_password(password):
            return None
        return user

    async def login(self, username: str, password: str) -> Optional[dict]:
        """
        Log in a user and return a JWT token.

        Args:
            username (str): The username.
            password (str): The password.

        Returns:
            Optional[dict]: Dictionary containing the access_token and token_type, or None if login fails.
        """
        user = await self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = self.create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
    

    async def register(self, user_data: UserPublic) -> User:
        """
        Register a new user.

        Args:
            user_data (UserCreate): The user registration data.

        Returns:
            User: The created user.

        Raises:
            HTTPException: If the user already exists or registration fails.
        """
        
        existing_user = await self.repository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists",
            )

        db_user = User(
            username=user_data.username
        )

        db_user.set_password(user_data.password)
        return await self.repository.create(db_user)