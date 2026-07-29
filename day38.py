from main import ask_claude

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

count = {
    "fail": 0,
    "pass":0
}

for case in test_cases:
    answer = ask_claude(case['question'])
    if case['expected'].lower() in answer.lower():
        count["pass"]+=1
    else:
        count["fail"]+=1

print(count)