from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
open_ai_client = OpenAI()


test_case = [
    {"question":"What is the capital of India", "answer": "Delhi", "human_verdict": True},
    {"question":"Where is eiffel tower located at", "answer": "Paris", "human_verdict": True},
    {"question":"Pyramid is just a myth does actually exist", "answer": "No they are real situated in Africa", "human_verdict": False},
    {"question":"Bali is part which country", "answer": "Indonasia", "human_verdict": True}
]


verdict = {
    "agreed": 0,
    "disagreed": 0
}

def ask_gpt(question,answer):
    prompt = f"""you are an AI reviewer which review response from another AI and judge whether they are correct or not
    once analyzed just provide respone in either true or false one word
    question is {question} and answer for that is {answer}"""
    response = open_ai_client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role":"user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip().lower() == "true"

def analyze_response(ai_response, human_verdict):
    if(ai_response == human_verdict):
        verdict["agreed"] +=1
    else:
        verdict["disagreed"] +=1

for test in test_case:
    response = ask_gpt(test['question'],test['answer'])
    analyze_response(response,test['human_verdict'])

print(verdict)
