from fastapi import FastAPI
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
from langfuse import observe
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor

load_dotenv()

AnthropicInstrumentor().instrument()

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

@observe()
def ask_claude(question: str):
    response = client.messages.create(
        model= 'claude-sonnet-4-5',
        max_tokens= 1024,
        messages=[
            {"role":"user", "content":question}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    print(ask_claude("What is the capital of france"))
    from langfuse import get_client
    get_client().flush()