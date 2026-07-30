from openai import OpenAI
from dotenv import load_dotenv
from main import ask_claude

load_dotenv()
open_ai_client = OpenAI()

test_cases = [
    {
        "question": "What is the capital of scotland",
        "expected": "Edinburgh"
    },
    {
        "question": "Capital of India",
        "expected": "Delhi"
    },
    {
        "question": "Currency used in dublin",
        "expected": "Euro"
    },
]

scorer = {}

def judge(question,answer,expected):
    prompt = f"""You are a judge which give score on other LLMs answers
    return only true or false nothing else
    Judge this questoin: {question}, got answer: {answer}, expected: {expected}"""
    response = open_ai_client.chat.completions.create(
        model='gpt-4o',
        messages=[{"role":"user", "content":prompt}]
    )
    return response.choices[0].message.content.strip().lower() == "true"

for cases in test_cases:
    response = ask_claude(cases['question'])
    scorer[cases['question']] = judge(cases['question'],response,cases['expected'])

print(scorer)

print(judge("What is the capital of Scotland?", "The capital is Glasgow.", "Edinburgh"))











