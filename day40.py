from openai import OpenAI
from dotenv import load_dotenv
from main import ask_claude

load_dotenv()

openAI_client = OpenAI()

judge_test_set = [
    # --- Correct answers: catch FALSE NEGATIVES (judge wrongly fails a right answer) ---
    {"question": "Capital of Italy?", "answer": "Rome", "human_verdict": True},
    {"question": "Which continent is Egypt in?", "answer": "Africa", "human_verdict": True},
    {"question": "What is 12 times 12?", "answer": "144", "human_verdict": True},

    # --- Obvious wrong answers: catch the RUBBER STAMP (blunt false positive) ---
    {"question": "What is the capital of Scotland?", "answer": "Glasgow", "human_verdict": False},
    {"question": "What is 12 times 12?", "answer": "100", "human_verdict": False},

    # --- Plausible wrong answers: catch a judge that's FUZZY ON THE FACT ---
    {"question": "Capital of Italy?", "answer": "Milan", "human_verdict": False},
    {"question": "Capital of Australia?", "answer": "Sydney", "human_verdict": False},
    {"question": "Who wrote Romeo and Juliet?", "answer": "Christopher Marlowe", "human_verdict": False},
]

def judge(question,answer):
    prompt = f"""You are judge for another LLM answer you will have question and answer provided by the LLM and you need just provide
    answer in one work true or false, here is the question {question} answer for it is {answer}"""
    open_ai_response = openAI_client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    return open_ai_response.choices[0].message.content.strip().lower() == "true"

total_true_false = {
    "agree":0,
    "disagree":0
}

for test in judge_test_set:
    judge_verdict = judge(test['question'],test['answer'])
    print(judge_verdict, test['question'])
    if(judge_verdict == test['human_verdict']):
        total_true_false['agree'] += 1
    else:
        total_true_false['disagree'] +=1

print(total_true_false)
    
