# emotion_api.py

import os
from dotenv import load_dotenv
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Set up model and tokenizer
emotion_classification_model = AutoModelForSequenceClassification.from_pretrained("fine-tuned-tinybert")
tokenizer = AutoTokenizer.from_pretrained("fine-tuned-tinybert")

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
emotion_classification_model.to(device)

# Set up Google Generative AI Model
gpt_model = ChatGoogleGenerativeAI(model="gemini-pro")
output_parser = StrOutputParser()
prompt_template = """You are a personal assistant, your job is to help the user with anything they ask.
                    Your response should be to make the user happy, the user's current emotion is {emotion}.
                    The user's statement is as follows:
                    {user_prompt}"""
prompt = ChatPromptTemplate.from_template(prompt_template)

# FastAPI app instance
app = FastAPI()

# Request schema for user input
class UserInput(BaseModel):
    prompt: str

# Predict emotion function
def predict_emotion(text: str) -> str:
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}

    emotion_classification_model.eval()

    with torch.no_grad():
        outputs = emotion_classification_model(**inputs)
        logits = outputs.logits

    prediction = torch.argmax(logits, dim=-1).item()
    label_names = ["sadness", "joy", "love", "anger", "fear", "surprise"]
    predicted_label = label_names[prediction]

    return predicted_label

# FastAPI endpoint
@app.post("/generate-response/")
async def generate_response(user_input: UserInput):
    try:
        # Step 1: Predict emotion
        emotion = predict_emotion(user_input.prompt)

        # Step 2: Generate response from the model
        chain = prompt | gpt_model | output_parser
        ai_response = chain.invoke({"emotion": emotion, "user_prompt": user_input.prompt})

        # Step 3: Return the response as JSON
        return {"emotion": emotion, "response": ai_response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

