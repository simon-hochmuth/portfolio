from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

'''
This code sets up a FastAPI application that uses a pre-trained sentiment analysis model from Hugging Face's Transformers library. The application accepts text input and returns the sentiment label and score.
My initial code for training is below in this comment block, but it is not needed for the FastAPI app to function.

# Load sentiment pipeline
classifier = pipeline("sentiment-analysis")

# Create API
app = FastAPI()

@app.post("/predict")
def predict(input: InputText):
    result = classifier(input.text)
    return {"label": result[0]["label"], "score": result[0]["score"]}
'''
# Define request body
class InputText(BaseModel):
    text: str

# Load your custom-trained model
classifier = pipeline("sentiment-analysis", model="./my_sentiment_model")

# Create API
app = FastAPI()

@app.post("/predict")
def predict(input: InputText):
    result = classifier(input.text)
    return {"label": result[0]["label"], "score": result[0]["score"]}
