import requests
import json

def ask(prompt, model="qwen3:0.6b", system=None, temp=0, max_token=200):
    r = requests.post(
        "http://localhost:11434/v1/chat/completions",
        json={
            "model": model,
            "messages": ([{"role": 'system', "content": system}] if system else []) + [{"role": "user","content": prompt }],
            "temperature": temp,
            "max_token": max_token

        },
        timeout=120
    )
    
    return r.json()["choices"][0]["message"]["content"]


SYSTEM_JSON = """You output ONLY valid JSON. No prose. No markdown fences.
Schema: {"sentiment": "pos"|"neg"|"neu", "confidence": number 0.0-1.0}
Example input: "Great pizza, slow service."
Example output: {"sentiment": "neu", "confidence": 0.7}"""

# print(ask("bad soup", system=SYSTEM_JSON))
my_prompt = "I kinda like this movie"
my_prompt = "Pick a color , be creative"

for i in [0.3, 1.0, 1.5]:
    print(f"temp: {i}")
    # raw = ask(my_prompt, system=SYSTEM_JSON, temp=i)
    raw = ask(my_prompt, temp=i)
    print(my_prompt)
    # print(json.loads(raw))
    print(raw)