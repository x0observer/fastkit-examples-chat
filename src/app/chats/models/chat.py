from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.middleware.engine import Base


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_group = Column(Boolean, default=False)
    participants = relationship("User", secondary="chat_participants")
    updated_at = Column(Integer, default=lambda: int(
        datetime.now().timestamp()), onupdate=lambda: int(datetime.now().timestamp()))
    created_at = Column(Integer, default=lambda: int(
        datetime.now().timestamp()))


class ChatParticipant(Base):
    __tablename__ = "chat_participants"
    chat_id = Column(Integer, ForeignKey("chats.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    updated_at = Column(Integer, default=lambda: int(
        datetime.now().timestamp()), onupdate=lambda: int(datetime.now().timestamp()))
    created_at = Column(Integer, default=lambda: int(
        datetime.now().timestamp()))


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    updated_at = Column(Integer, default=lambda: int(
        datetime.now().timestamp()), onupdate=lambda: int(datetime.now().timestamp()))
    created_at = Column(Integer, default=lambda: int(
        datetime.now().timestamp()))
    # is_read = Column(Boolean, default=False)
