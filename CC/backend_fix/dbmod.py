from os import link
from turtle import back
from typing import List, Optional, Union
from sqlalchemy import table
from sqlmodel import Field, Relationship, SQLModel, Column, JSON
import datetime

class StoryActivitiesLink(SQLModel, table=True):
    story_id: Optional[int] = Field(default=None, foreign_key="story.id", primary_key=True)
    activity_id: Optional[int] = Field(default=None, foreign_key="activity.id", primary_key=True)

class StoryTagLink(SQLModel, table=True):
    story_id: Optional[int] = Field(default=None, foreign_key="story.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

class QuoteTagLink(SQLModel, table=True):
    quote_id: Optional[int] = Field(default=None, foreign_key="quote.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

#----------------------------------------------------------------------------------------------

class UserBase(SQLModel):
    username: str
    name: str = Field(index=True)
    biography: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: str = datetime.datetime.now().date()
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

class TagBase(SQLModel):
    tag: str

class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quotes: List["Quote"] = Relationship(back_populates="tags", link_model=QuoteTagLink)
    stories: List["Story"] = Relationship(back_populates="tags", link_model=StoryTagLink)

class TagCreate(TagBase):
    pass

class TagGet(TagBase):
    pass

#----------------------------------------------------------------------------------------------

class Quote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: str = datetime.datetime.now().date()
    quote_text: str
    category: Union[str, None]
    tags: List[Tag]  = Relationship(back_populates="quotes", link_model=QuoteTagLink)
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
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: str = datetime.datetime.now().date()
    img_url: Union[str, None]
    stories: List["Story"] = Relationship(back_populates="activities", link_model=StoryActivitiesLink)

class ActivityCreate(ActivityBase):
    pass

class ActivityGet(ActivityBase):
    id: int

#----------------------------------------------------------------------------------------------

class Story(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    story_text: str
    created_at: str = datetime.datetime.now().date()
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="stories")
    quote_id: Optional[int] = Field(default=None, foreign_key="quote.id")
    quote: Optional[Quote] = Relationship(back_populates="stories")
    activities: List[Activity] = Relationship(back_populates="stories", link_model=StoryActivitiesLink)
    tags: List[Tag] = Relationship(back_populates="stories", link_model=StoryTagLink) 

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
    created_at: str
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
    quote: Union[QuoteCreate, None]

class HistoryDetailed(History):
    activities: Optional[List[ActivityCreate]]
    tags: Union[List[Tag], None]

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
    stories: Optional[HistoryDetailed]

class StoryPostReturn(SQLModel):
    message: str
    story: Union[HistoryDetailed, None]