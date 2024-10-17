
# Import Libraries
import os
from src.helper import load_pdf_file, download_huggingface_embedding, text_split
from src.prompt import *
from flask import Flask, render_template, request, jsonify
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Initialize flask app
app = Flask(__name__)

# Set up environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY   

# Download embedding model
embedding = download_huggingface_embedding()

# Load pinecone index
index_name = "medical-chatbot-implementation"

# Initialize a PineconeVectorStore instance from the provided documents and embedding model.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,  # The name of the existing index to connect to.
    embedding=embedding,     # The embedding model used to convert documents into vector representations.
)

# Set a retriver object
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize OpenAI client
llm = OpenAI(temperature=0, max_tokens=500)

# Set up a chat prompt template using the ChatPromptTemplate class
prompt = ChatPromptTemplate.from_messages([
    # Define the system message with the system prompt
    ("system", system_prompt),
    
    # Define the user message, where {input} will be replaced with actual user input
    ("human", "{input}"),
])

# Set up a question-answer chain using the create_stuff_documents_chain function
question_answer_chain = create_stuff_documents_chain(
    # Specify the language model to be used for generating responses
    llm=llm, 
    
    # Provide the prompt that will guide the question-answering process
    prompt=prompt, 
)

# Set up a retrieval chain using the create_retrieval_chain function
rag_chain = create_retrieval_chain(
    # Provide the retriever, which is responsible for fetching relevant documents or data
    retriever,
    
    # Include the question-answer chain that will process the retrieved information
    question_answer_chain,
)

# Set up the Flask app's homepage route
@app.route("/")
def index():
    # Render and return the 'chat.html' template when the homepage is accessed
    return render_template("chat.html")

# Chat operations: Define a route for handling chat messages
@app.route("/get", methods=["GET", "POST"])
def chat():
    # Retrieve the message sent from the client via form data
    msg = request.form['msg']
    
    # Store the message in a variable for further processing
    input = msg
    
    # Print the input message to the console for debugging purposes
    print(input)
    
    # Invoke the retrieval-augmented generation chain with the input message
    response = rag_chain.invoke({"input": msg})
    
    # Print the response answer to the console for debugging purposes
    print("Response : ", response['answer'])
    
    # Return the generated answer as a string to the client
    return str(response['answer'])


# Run the Flask application
if __name__ == "__main__":
    # Start the Flask app, making it accessible on all network interfaces
    # Set the port to 8080 and enable debug mode for easier development
    app.run(host="0.0.0.0", port=8080, debug=True)