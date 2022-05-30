from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, Field, select
from db import create_db_and_tables, engine
import models

app = FastAPI()
def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register", response_model=models.UserGetWithoutStories)
def register_user(*, session: Session = Depends(get_session), user: models.UserRegister):
    hashed_pass = user.hashed_password + "amee3z1ng"
    db_user = models.User(username=user.username, name=user.name, biography=user.biography, hashed_password=hashed_pass)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

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

@app.post("/user/{user_id}/story")
def post_story(*, session: Session = Depends(get_session), story: models.StoryRegister, user_id):
    db_story = models.Story(user_id=user_id, story_text=story.story_text)
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story

@app.get("/story/{story_id}", response_model=models.StoryGetWithoutUser)
def get_story(*, session: Session = Depends(get_session), story_id):
    story = session.get(models.Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="This aren't the story you're looking for")
    return story