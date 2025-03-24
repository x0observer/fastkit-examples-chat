
from datetime import datetime
from sqlalchemy import Column, Integer, String
from src.middleware.engine import Base
from src.app.auth.externals.pwd_context import pwd_context


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    updated_at = Column(Integer, default=lambda: int(datetime.now().timestamp()), onupdate=lambda: int(datetime.now().timestamp()))
    created_at = Column(Integer, default=lambda: int(datetime.now().timestamp()))
                        
    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)
