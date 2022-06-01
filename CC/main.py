from email import message
from turtle import st
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, Field, select
from datetime import datetime, date
from passlib.context import CryptContext
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED,HTTP_404_NOT_FOUND
from db import create_db_and_tables, engine
import models

app = FastAPI()
def get_session():
    with Session(engine) as session:
        yield session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register", response_model=models.UserReturnRegister)
def register_user(*, session: Session = Depends(get_session), user: models.UserRegister):
    hashed_pass = Hasher.get_password_hash(user.hashed_password)
    db_user = models.User(username=user.username, name=user.name, biography=user.biography, hashed_password=hashed_pass)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return models.UserReturnRegister(message="OK", id=db_user.id)

@app.get("/users", response_model=List[models.UserGet])
def get_users(*, session: Session = Depends(get_session)):
    users = session.exec(select(models.User)).all()
    return users

@app.get("/user/{user_id}", response_model=models.UserGetWithoutStories)
def get_a_user(*, session: Session = Depends(get_session), user_id):
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/login/")
def user_login(*, session: Session = Depends(get_session), user: models.UserLogin):
    opr = select(models.User).where(models.User.username == user.username)
    user_found =  session.exec(opr).first()
    if not user_found:
        return JSONResponse(status_code=401, content={"message":"Invalid username and/or password"})
    check_password = Hasher.verify_password(user.password, user_found.hashed_password)
    if not check_password:
        return JSONResponse(status_code=401, content={"message":"Invalid username and/or password"})
    return models.UserReturnRegister(message="OK", id=user_found.id)

@app.post("/user/{user_id}/story")
def post_story(*, session: Session = Depends(get_session), story: models.StoryRegister, user_id):
    db_story = models.Story(user_id=user_id, story_text=story.story_text)
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story

@app.get("/user/{user_id}/stories")
def get_user_stories(*, session: Session = Depends(get_session), user_id, detailed: bool = None):
    user = session.get(models.User, user_id)
    if not user.stories:
        raise HTTPException(status_code=404, detail="No story was found")
    if detailed:
        return models.StoryReturnDetailed(message="OK", stories=user.stories)
    return models.StoryReturn(message="OK", stories=user.stories)

@app.get("/story/{story_id}", response_model=models.StoryGetWithoutUser)
def get_story(*, session: Session = Depends(get_session), story_id):
    story = session.get(models.Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="This aren't the story you're looking for")
    return story

@app.post("/story/{story_id}/quote", response_model=models.QuoteGetWithoutStories)
def post_quote(*, session: Session = Depends(get_session), quote: models.QuoteCreate, story_id):
    db_quote = models.Quote(quote_text=quote.quote_text)
    db_story = session.get(models.Story, story_id)
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")
    db_story.quote_id = story_id
    session.add(db_quote)
    session.commit()
    session.refresh(db_quote)
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_quote

@app.get("/quote", response_model=List[models.QuoteGet])
def get_quotes(*, session: Session = Depends(get_session)):
    quotes = session.exec(select(models.Quote)).all()
    return quotes

@app.get("/quote/{quote_id}", response_model=models.QuoteGetWithoutStories)
def get_quote(*, session: Session = Depends(get_session), quote_id):
    quote = session.get(models.Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote