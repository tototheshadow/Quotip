from lib2to3.pgen2.token import OP
from turtle import back
from typing import List, Optional
from sqlalchemy import table
from sqlmodel import Field, Relationship, SQLModel

class UserBase(SQLModel):
    username: str
    name: str = Field(index=True)
    biography: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    stories: List["Story"] = Relationship(back_populates="user")
    hashed_password: str

class UserRegister(UserBase):
    hashed_password: str

class UserGet(UserBase):
    id: int

class UserUpdate(SQLModel):
    username: Optional[str] = None
    name: Optional[str] = None
    biography: Optional[str] = None


class Quote(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    quote_text: str


class Story(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    story_text: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="stories")
    quote_id: Optional[int] = Field(default=None, foreign_key="quote.id")
 
class StoryRegister(SQLModel):
    story_text: str

class StoryGet(SQLModel):
    id: int
    story_text: str
    user_id: int

class UserGetWithoutStories(UserGet):
    stories: List[StoryGet] = []

class StoryGetWithoutUser(StoryGet):
    user: Optional[UserGet] = None
