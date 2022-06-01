from email.quoprimime import quote
from lib2to3.pgen2.token import OP
from turtle import back
from typing import List, Optional
from sqlalchemy import table
from sqlmodel import Field, Relationship, SQLModel
import datetime

class UserBase(SQLModel):
    username: str
    name: str = Field(index=True)
    biography: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime.datetime = datetime.datetime.now()
    stories: List["Story"] = Relationship(back_populates="user")
    hashed_password: str

class UserRegister(UserBase):
    hashed_password: str
 
class UserLogin(SQLModel):
    username: str
    password: str

class UserGet(UserBase):
    id: int

class UserUpdate(SQLModel):
    username: Optional[str] = None
    name: Optional[str] = None
    biography: Optional[str] = None

#----------------------------------------------------------------------------------------------

class Quote(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    created_at: datetime.datetime = datetime.datetime.now()
    quote_text: str
    stories: List["Story"] = Relationship(back_populates="quote")

class QuoteCreate(SQLModel):
    quote_text: str

class QuoteGet(SQLModel):
    id: int
    quote_text: str

#----------------------------------------------------------------------------------------------

class ActivityBase(SQLModel):
    activity: str

class Activity(ActivityBase, table=True):
    id: int = Field(primary_key=True, index=True)
    created_at: datetime.datetime = datetime.datetime.now()
    story: Optional["Story"] = Relationship(back_populates="activities")

class ActivityCreate(ActivityBase):
    pass

class ActivityGet(ActivityBase):
    id: int

#----------------------------------------------------------------------------------------------

class Story(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    story_text: str
    created_at: datetime.datetime = datetime.datetime.now()
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="stories")
    quote_id: Optional[int] = Field(default=None, foreign_key="quote.id")
    quote: Optional[Quote] = Relationship(back_populates="stories")
    activities_id: List[int] = Field(default=None, foreign_key="activity.id")
    activities: List[Activity] = Relationship(back_populates="story")

 
class StoryRegister(SQLModel):
    story_text: str

class StoryGet(SQLModel):
    id: int
    story_text: str
    user_id: int

class StoryUpdate(SQLModel):
    story_text: Optional[str]
    quote_id: Optional[int]
    
#----------------------------------------------------------------------------------------------

class UserGetWithoutStories(UserGet):
    stories: List[StoryGet] = []

class StoryGetWithoutUser(StoryGet):
    user: Optional[UserGet] = None
    quote: Optional[QuoteGet] = None

class QuoteGetWithoutStories(QuoteGet):
    stories: List[StoryGet] = []

#----------------------------------------------------------------------------------------------

class StoryGetHistory(SQLModel):
    id: int
    story_text: str

class History(StoryGetHistory):
    quote: Optional[QuoteCreate] = None

class HistoryDetailed(History):
    activitiy: Optional[List[ActivityBase]] = None

class UserReturnRegister(SQLModel):
    message: str
    id: Optional[int] = None

class UserReturnStories(SQLModel):
    message: str
    id: int

class StoryReturn(SQLModel):
    message: str
    stories: List[History] = []

class StoryReturnDetailed(SQLModel):
    message: str
    stories: List[HistoryDetailed] = []

