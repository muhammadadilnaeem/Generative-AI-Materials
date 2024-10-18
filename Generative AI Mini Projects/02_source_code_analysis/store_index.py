
# Import Libraries
import os
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from src.helper import repo_ingestion, load_repo, text_splitter, load_embedding

# Load Environment Variables
load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# url = "https://github.com/entbappy/End-to-end-Medical-Chatbot-Generative-AI"

# repo_ingestion(url)


# Load documents from the specified repository directory.
# The `load_repo` function retrieves all relevant documents from "repo/".
documents = load_repo("repo/")

# Split the loaded documents into smaller text chunks for processing.
# The `text_splitter` function is responsible for dividing the documents into manageable parts.
text_chunks = text_splitter(documents)

# Load the embedding model to convert text into vector representations.
# The `load_embedding` function initializes and returns the embedding model.
embeddings = load_embedding()

# Create a Chroma database from the provided text chunks.
# `text_chunks` contains the documents or text data to be stored.
# `embeddings` is the embedding model used to convert text into vector representations.
# `persist_directory` specifies the directory where the database will be stored.

vectordb = Chroma.from_documents(text_chunks, embedding=embeddings, persist_directory='./db')

# Save the database to the specified directory, ensuring data is persisted for future use.
vectordb.persist()