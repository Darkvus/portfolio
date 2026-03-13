from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    slug: Optional[str] = None
    content: str
    content_es: Optional[str] = None
    excerpt: Optional[str] = None
    tags: Optional[str] = None
    cover_image: Optional[str] = None
    published: bool = False


class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    content_es: Optional[str] = None
    excerpt: Optional[str] = None
    tags: Optional[str] = None
    cover_image: Optional[str] = None
    published: Optional[bool] = None


class PostOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    excerpt: Optional[str]
    tags: Optional[str]
    cover_image: Optional[str]
    published: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PostAdminOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    content_es: Optional[str]
    excerpt: Optional[str]
    tags: Optional[str]
    cover_image: Optional[str]
    published: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SubscribeRequest(BaseModel):
    email: str


class SubscribeOut(BaseModel):
    message: str


class SubscriberOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ProfileOut(BaseModel):
    open_to_work: bool
    location: str
    available_from: Optional[str]


class ProfileUpdate(BaseModel):
    open_to_work: Optional[bool] = None
    location: Optional[str] = None
    available_from: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginData(BaseModel):
    username: str
    password: str
