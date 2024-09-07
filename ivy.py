import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

emotion_classification_model = AutoModelForSequenceClassification.from_pretrained("fine-tuned-tinybert")
tokenizer = AutoTokenizer.from_pretrained("fine-tuned-tinybert")

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
emotion_classification_model.to(device)

def predict_emotion(text):
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

from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-pro")

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt_template = """You are a personal assistant, your job is to help the user with anything they ask.
                    Your response should be to make the user happpy, the user's current emotion is {emotion}
                    The user's statement is as follows:
                    {user_prompt}"""

prompt = ChatPromptTemplate.from_template(prompt_template)
output_parser = StrOutputParser()

chain = prompt | model | output_parser

prompt = input("Enter your prompt: ")
emotion = predict_emotion(prompt)

print(chain.invoke({"emotion": emotion, "user_prompt": prompt}))