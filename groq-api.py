import os
from dotenv import load_dotenv

from groq import Groq

# Load environment variables from .env file
load_dotenv()

grop_api_key = os.getenv('GROQ_API_KEY')

client = Groq(
    api_key=grop_api_key,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)
