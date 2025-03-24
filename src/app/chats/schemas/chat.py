from pydantic import BaseModel



class ChatCreate(BaseModel):
    name: str

    # class Config:
    #     from_attributes = True


class ChatRead(ChatCreate):
    id: int

    # class Config:
    #     from_attributes = True
    
class MessageCreate(BaseModel):
    chat_id: int
    text: str
    
class MessageRead(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: int
    updated_at: int