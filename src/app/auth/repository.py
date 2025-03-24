
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.fastkit.repositories.base import BaseRepository
from src.app.auth.models.user import User

class AuthRepository(BaseRepository[User]):
    """
        ...
    """
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(User, db_session)


    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username using a raw SQL query.

        Args:
            username (str): The username to search for.

        Returns:
            Optional[User]: The user if found, otherwise None.
        """

        sql = text("""
            SELECT id, username, hashed_password
            FROM users
            WHERE username = :username
        """)


        result = await self.uow.db.execute(sql, {"username": username})
        row = result.fetchone()

        if row:
            # ...
            user_dict = dict(zip(result.keys(), row))
            return User(**user_dict)
        return None