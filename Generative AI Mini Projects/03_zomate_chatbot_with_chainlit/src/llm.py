# Import necessary libraries
import os  # For interacting with the operating system
from openai import OpenAI  # OpenAI library for accessing GPT models
from dotenv import load_dotenv  # For loading environment variables from a .env file
from src.prompt import system_instruction  # Importing system instructions from a local module

# Initialize the OpenAI client
client = OpenAI()

# Prepare the initial message for the chat
messages = [{"role": "user", "content": system_instruction}]

def ask_order(messages, model="gpt-4o-mini", temperature=0.1):
    """
    Function to send a message to the OpenAI chat model and retrieve a response.
    
    Parameters:
    - messages (dict): The messages to send to the model.
    - model (str): The model to use for generating the response; defaults to "gpt-4o-mini".
    - temperature (float): Controls the randomness of the output; lower values make the output more deterministic.
    
    Returns:
    - str: The content of the model's response.
    """
    # Create a chat completion request to the OpenAI model
    response = client.chat.completions.create(
        model=model,  # Specify the model to use
        messages=messages,  # Provide the messages for the model
        temperature=temperature  # Set the temperature for response variability
    )
    
    # Return the content of the first choice from the response
    return response.choices[0].message.content