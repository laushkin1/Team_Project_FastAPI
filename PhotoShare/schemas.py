from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from typing import List


class CommentRequest(BaseModel):
    comment: str


class CommentResponce(BaseModel):
    comment: str



class AdminComment(CommentResponce):
    id: int


class TagRequest(BaseModel):
    name: str


class TagResponce(BaseModel):
    id: int
    tags: str


class Admin(BaseModel):
    id: int
    role: str


class GetRole(BaseModel):
    role: str


class PhotoRequest(BaseModel):
    description: str
    

class PhotoModel(BaseModel):
    id: int
    url: str
    image_qr: Optional[str] = None
    description: Optional[str] = None
    comments: List[CommentResponce] = []
    tags: List[TagRequest] = []
    created_at: datetime
    updated_at: Optional[datetime] = None


class AdminPhotosModel(BaseModel):
    id: int
    url: str
    image_qr: Optional[str] = None
    description: Optional[str] = None
    comments: List[AdminComment] = []
    tags: List[TagRequest] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

class ShareResponce(BaseModel):
    id: int
    url: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None 


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)



class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
