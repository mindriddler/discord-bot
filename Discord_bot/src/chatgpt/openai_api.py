import os

import openai
from dotenv import load_dotenv
from utils.utils import read_config

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai_config = read_config("openai")


def chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model=openai_config["model"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=openai_config["temperature"],
        max_tokens=openai_config["max_tokens"],
    )
    response_dict = response.choices
    prompt_response = ""  # Initialize the variable with an empty string
    if response_dict and len(response_dict) > 0:
        prompt_response = response_dict[0].message["content"]
    return prompt_response.strip()
