from typing import List, Optional, Union
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlmodel import Session, Field, select, func
from passlib.context import CryptContext
from starlette.responses import JSONResponse
from db import create_db_and_tables, create_quotes, create_tags, engine
import dbmod
import pickle
import numpy as np
import tensorflow as tf
import re

app = FastAPI(title="Quotip API", version="0.1")
def get_session():
    with Session(engine) as session:
        yield session

def preprocess_text(sen):
    sentence = remove_tags(sen)
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
    sentence = re.sub(r'\s+', ' ', sentence)
    return sentence
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

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
    #create_quotes()
    #create_tags()

@app.post("/register", response_model=dbmod.UserReturnRegister)
def register_user(*, session: Session = Depends(get_session), user: dbmod.UserRegister):
    opr = select(dbmod.User)
    users = session.exec(opr).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username already exist')
    hashed_pass = Hasher.get_password_hash(user.hashed_password)
    db_user = dbmod.User(username=user.username, name=user.name, biography=user.biography, hashed_password=hashed_pass)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return dbmod.UserReturnRegister(message="OK", id=db_user.id)

@app.get("/users", response_model=List[dbmod.UserGet])
def get_users(*, session: Session = Depends(get_session)):
    users = session.exec(select(dbmod.User)).all()
    return users

@app.get("/user/{user_id}", response_model=dbmod.UserGetWithoutStories)
def get_a_user(*, session: Session = Depends(get_session), user_id):
    user = session.get(dbmod.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/login/")
def user_login(*, session: Session = Depends(get_session), user: dbmod.UserLogin):
    opr = select(dbmod.User).where(dbmod.User.username == user.username)
    user_found =  session.exec(opr).first()
    if not user_found:
        return JSONResponse(status_code=401, content={"message":"Invalid username and/or password"})
    check_password = Hasher.verify_password(user.password, user_found.hashed_password)
    if not check_password:
        return JSONResponse(status_code=401, content={"message":"Invalid username and/or password"})
    return dbmod.UserReturnRegister(message="OK", id=user_found.id)


@app.post("/user/{user_id}/story", response_model=dbmod.StoryPostReturn)
def post_story(*, session: Session = Depends(get_session), story: dbmod.StoryRegister, user_id, qtags: Union[List[int], None] = Query(default=None)):
    with open('tokenizer.pickle', 'rb') as handle:
        Tokenizer = pickle.load(handle)

    model = tf.keras.models.load_model("model_final.model")

    padding_type='post'
    max_length = 32

    sentence = story.story_text
    sentence = preprocess_text(sentence)

    sentence_processed = Tokenizer.texts_to_sequences([sentence])
    sentence_processed = np.array(sentence_processed)
    sentence_padded = tf.keras.preprocessing.sequence.pad_sequences(sentence_processed, padding=padding_type, maxlen=max_length)
    predicted = model.predict(sentence_padded)
    no_class = np.argmax(predicted)
    if no_class == 1:
        emotion = 'joy'
    elif no_class == 2:
        emotion = 'sadness'
    elif no_class == 3:
        emotion = 'anger'
    elif no_class == 4:
        emotion = 'fear'
    elif no_class == 5:
        emotion = 'love'
    else :
        emotion = 'surprise'

    db_story = dbmod.Story(user_id=user_id, story_text=story.story_text)
    if qtags:
        taglist = []
        for i, q in enumerate(qtags):
            taglist.append(session.get(dbmod.Tag, q))
            db_story.tags.append(taglist[i])
        quotez = session.exec(select(dbmod.Quote).where(dbmod.Quote.category == emotion).order_by(func.random())).all()
        for qtz in quotez:
            for tgz in qtz.tags:
                if tgz.id == qtags[0]:
                    db_story.quote_id = qtz.id
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return dbmod.StoryPostReturn(message="OK", story=db_story)

@app.get("/user/{user_id}/stories")
def get_user_stories(*, session: Session = Depends(get_session), user_id, story_detailed_id: int = None):
    user = session.get(dbmod.User, user_id)
    if not user.stories:
        return JSONResponse(status_code=404, content={"message":"No detailed story was found"})
    if story_detailed_id:
        story_detailed =  session.get(dbmod.Story, story_detailed_id)
        if not story_detailed.activities or not story_detailed:
            return JSONResponse(status_code=404, content={"message":"No detailed story was found"})
        return dbmod.StoryReturnDetailed(message="OK", stories=story_detailed)
    return dbmod.StoryReturn(message="OK", stories=user.stories)

@app.get("/story/{story_id}", response_model=dbmod.StoryGetWithoutUser)
def get_story(*, session: Session = Depends(get_session), story_id):
    story = session.get(dbmod.Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="This aren't the story you're looking for")
    return story


@app.post("/story/{story_id}/quote", response_model=dbmod.QuoteGetWithoutStories)
def post_quote(*, session: Session = Depends(get_session), quote: dbmod.QuoteCreate, story_id):
    db_quote = dbmod.Quote(quote_text=quote.quote_text)
    db_story = session.get(dbmod.Story, story_id)
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

@app.get("/quote", response_model=List[dbmod.QuoteGet])
def get_quotes(*, session: Session = Depends(get_session)):
    quotes = session.exec(select(dbmod.Quote)).all()
    return quotes

@app.get("/quote/{quote_id}", response_model=dbmod.QuoteGetWithoutStories)
def get_quote(*, session: Session = Depends(get_session), quote_id):
    quote = session.get(dbmod.Quote, quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@app.post("/post/activity", response_model=dbmod.Activity)
def post_activity(*, session: Session = Depends(get_session), activity: dbmod.ActivityCreate):
    opr = select(dbmod.Activity)
    activities = session.exec(opr).all()
    if any(x.activity == activity.activity for x in activities):
        raise HTTPException(status_code=400, detail='Activity already exist')
    db_activity = dbmod.Activity(activity=activity.activity)
    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return db_activity


@app.patch("/patch/story/{story_id}", response_model=dbmod.StoryGetHistory)
def patch_story(*, session: Session = Depends(get_session), story_id, activity_id: int):
    patch_story = session.get(dbmod.Story, story_id)
    activ = session.get(dbmod.Activity, activity_id)
    if not patch_story or not activ:
        raise HTTPException(status_code=404, detail="This aren't the story/activity you're looking for")
    patch_story.activities.append(activ)
    session.add(patch_story)
    session.commit()
    session.refresh(patch_story)
    return patch_story


@app.post("/post/tag", response_model=dbmod.Tag)
def post_tag(*, session: Session = Depends(get_session), tag: dbmod.TagCreate):
    opr = select(dbmod.Tag)
    tags = session.exec(opr).all()
    if any(x.tag == tag.tag for x in tags):
        raise HTTPException(status_code=400, detail='Tag already exist')
    db_tag = dbmod.Tag(tag=tag.tag)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

@app.get("/get/tag", response_model=List[dbmod.Tag])
def get_tags(*, session: Session = Depends(get_session)):
    tags = session.exec(select(dbmod.Tag)).all()
    return tags