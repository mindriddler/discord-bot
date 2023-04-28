import asyncio
import os
from functools import partial

import openai
from dotenv import load_dotenv

from utils.utils import read_config

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai_config = read_config("openai")


async def chatgpt_response(prompt):
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None,
        partial(
            openai.ChatCompletion.create,
            model=openai_config["model"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=openai_config["temperature"],
            max_tokens=openai_config["max_tokens"],
        ),
    )
    response_dict = response.choices
    prompt_response = ""
    if response_dict and len(response_dict) > 0:
        prompt_response = response_dict[0]["message"]["content"]
    return prompt_response.strip()