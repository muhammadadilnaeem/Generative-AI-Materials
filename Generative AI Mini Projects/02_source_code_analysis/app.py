# Import Libraries
import os
from dotenv import load_dotenv
from src.helper import load_embedding
from langchain.vectorstores import Chroma 
from src.helper import repo_ingestion
from flask import Flask, render_template, jsonify, request
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize Flask app
app = Flask(__name__)

# Load the OpenAI embeddings model using the previously defined function
embeddings = load_embedding()

# Specify the directory where the persisted database is stored
persist_directory = "db"

# Load the persisted vector database from disk using the specified directory and embeddings function
vectordb = Chroma(
    persist_directory=persist_directory,  # Directory from which to load the persisted database
    embedding_function=embeddings           # Function used for generating embeddings for the documents
)

# Initialize an instance of the ChatOpenAI language model
llm = ChatOpenAI()

# Create a memory object to store conversation history and enable summarization
memory = ConversationSummaryMemory(
    llm=llm,                     # The language model used for generating summaries of the conversation
    memory_key="chat_history",   # A key to identify the conversation history in the memory
    return_messages=True         # Indicates whether to include the actual messages in the summary
)

# Create a ConversationalRetrievalChain for question-answering with memory and document retrieval
qa = ConversationalRetrievalChain.from_llm(
    llm,                                           # The language model used to generate answers
    retriever=vectordb.as_retriever(              # Set up the retriever from the vector database
        search_type="mmr",                        # Specify the search algorithm; "mmr" stands for Maximum Marginal Relevance
        search_kwargs={"k": 8}                    # Additional search parameters; "k" defines the number of top results to return (8 in this case)
    ),
    memory=memory                                  # Pass the memory object to retain conversation context and history
)

# Define a route for the root URL ('/') of the web application
@app.route('/', methods=["GET", "POST"])
def index():
    # Render and return the 'index.html' template when this route is accessed
    return render_template('2index.html')

# # Define a route for the '/chatbot' URL of the web application
# @app.route('/chatbot', methods=["GET", "POST"])
# def gitRepo():
#     # Check if the request method is POST
#     if request.method == 'POST':
#         # Retrieve the user input from the form data under the key 'question'
#         user_input = request.form['question']
        
#         # Call the repo_ingestion function with the user input (assumed to be a repository URL)
#         repo_ingestion(user_input)
        
#         # Execute the 'store_index.py' script using the system shell to store embeddings or data
#         os.system("python store_index.py")

#     # Return a JSON response containing the user input as a string
#     return jsonify({"response": str(user_input)})


@app.route('/chatbot', methods=["GET", "POST"])
def gitRepo():
    if request.method == 'POST':
        user_input = request.form['question']
        
        # Show the processing message before executing the long process
        response_message = "Please Wait Your Data is being Processed 👁"
        
        # Call the repo_ingestion function
        repo_ingestion(user_input)
        
        # Execute the 'store_index.py' script to process the data
        os.system("python store_index.py")
        
        # Update the message once the process is complete
        response_message = "Processing Complete. Now you can Ask Questions ✔"
    
        # Send the final message as JSON response
        return jsonify({"response": response_message, "user_input": user_input})




# Define a route for the '/get' URL of the web application
@app.route("/get", methods=["GET", "POST"])
def chat():
    # Retrieve the message sent in the form data under the key 'msg'
    msg = request.form["msg"]
    
    # Store the retrieved message in the 'input' variable
    input = msg
    print(input)  # Print the input message to the console for debugging purposes

    # Check if the input is the command to clear the repository
    if input == "clear":
        # Execute a shell command to remove the 'repo' directory and its contents
        os.system("rm -rf repo")

    # Process the input through the question-answering system and store the result
    result = qa(input)
    
    # Print the answer obtained from the question-answering system to the console
    print(result['answer'])
    
    # Return the answer as a string response to the client
    return str(result["answer"])

# Check if the script is being run directly (not imported as a module)
if __name__ == '__main__':
    # Start the Flask web application
    app.run(
        host="0.0.0.0",  # Bind the server to all available network interfaces
        port=8080,       # Set the port number to 8080
        debug=True       # Enable debug mode for detailed error messages and auto-reload
    )