from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
app = FastAPI()

class Question(BaseModel):
    question: str




@app.post('/ask')
def ask(body: Question):
    answer = ask_claude(body.question)
    return {
        "response" : answer
    }

def ask_claude(question: str):
    response = client.messages.create(
        model= 'claude-sonnet-4-5',
        max_tokens= 1024,
        messages=[
            {"role":"user", "content":question}
        ]
    )
    return response.content[0].text

