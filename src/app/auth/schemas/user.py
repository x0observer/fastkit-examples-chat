from pydantic import BaseModel


class UserPublic(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    hashed_password: str
    # class Config:
    #     from_attributes = True


class UserRead(BaseModel):
    id: int
    username: str
    # class Config:
    #     from_attributes = True
    
class UserResponse(UserRead):
    pass


