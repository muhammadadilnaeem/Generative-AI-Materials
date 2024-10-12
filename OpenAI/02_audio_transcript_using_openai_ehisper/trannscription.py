# Import Libraries
import os 
from openai import OpenAI
client = OpenAI()

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load audio File
audio_file_path = r"E:\Practice python\Generative AI Materials\OpenAI\02_audio_transcript_using_openai_ehisper\Recording.m4a"
with open(audio_file_path, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

print(transcription.text)