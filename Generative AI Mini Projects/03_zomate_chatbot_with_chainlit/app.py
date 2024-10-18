import chainlit as cl  # Import the Chainlit library for building interactive web applications
from src.llm import ask_order, messages  # Import the ask_order function and messages list from the local LLM module

@cl.on_message  # Decorator to define an asynchronous function that handles incoming messages
async def main(message: cl.Message):
    """
    Main function to handle user messages and generate responses.
    
    Parameters:
    - message (cl.Message): The incoming message from the user.
    """
    # Append the user's message to the messages list with the role 'user'
    messages.append({"role": "user", "content": message.content})
    
    # Call the ask_order function to get a response from the LLM
    response = ask_order(messages)
    
    # Append the assistant's response to the messages list with the role 'assistant'
    messages.append({"role": "assistant", "content": response})
    
    # Send the assistant's response back to the user as a message
    await cl.Message(
        content=response,  # The content of the message to send
    ).send()  # Send the message asynchronously