import json
from main import ask_claude
import os

test_cases = [
    {"question": "Capital of Italy?", "expected": "Rome"},
    {"question": "Capital of Scotland?", "expected": "Edinburgh"},
    {"question": "What is 12 times 12?", "expected": "144"},
]

response_record = []


def run_eval(cases, question_key, response_key):
    records = []
    for case in cases:
        claude_response = ask_claude(case[question_key])
        if case[response_key].lower() in claude_response.lower():
            records.append({"question": case[question_key], "passed": True})
        else:
            records.append({"question": case[question_key], "passed": False})
    return records


if not os.path.exists("baseline.json"):
    result = run_eval(test_cases, "question", "expected")
    with open("baseline.json", "w") as f:
        json.dump(result, f, indent=2)
else:
    result = run_eval(test_cases, "question", "expected")
    with open("baseline.json", "r") as f:
        baseline = json.load(f)

    for old, new in zip(baseline, result):
        if old["passed"] == True and new["passed"] == False:
            print("REGRESSION:", new["question"])
