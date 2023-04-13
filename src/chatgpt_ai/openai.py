import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("CHATGPT_API_KEY")


def chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        max_tokens=100,
    )
    response_dict = response.choices
    if response_dict and len(response_dict) > 0:
        prompt_response = response_dict[0].message["content"]
    return prompt_response.strip()
