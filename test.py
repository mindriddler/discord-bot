import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("CHATGPT_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
    ],
    temperature=1,
    max_tokens=4000,
)

print(response.choices[0].text.strip())
