# Import Libraries
import os 
from openai import OpenAI
client = OpenAI()

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a program pythonto sum 2 numbers."
        }
    ]
)

print(completion.choices[0].message)