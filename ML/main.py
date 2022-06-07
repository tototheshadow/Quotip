import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
import tensorflow as tf
import re

app = FastAPI()
class Emotion(BaseModel):
    sentence: str

@app.get('/')
def index():
    return {'message' : 'Hello World'}
    

@app.get('/predict')
def predict():
    with open('tokenizer.pickle', 'rb') as handle:
        Tokenizer = pickle.load(handle)

    model = tf.keras.models.load_model("model_final.model")

    padding_type='post'
    max_length = 32

    sentence = 'i feel shocked'
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
    print(emotion)
    return {
    'prediction': emotion,
}

def preprocess_text(sen):
    sentence = remove_tags(sen)

    sentence = re.sub('[^a-zA-Z]', ' ', sentence)

    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)

    sentence = re.sub(r'\s+', ' ', sentence)

    return sentence
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)