
# Import Libraries
import os
from git import Repo
from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Function to clone a GitHub repository into a local directory
def repo_ingestion(repo_url):
    # Create a directory named "repo" if it doesn't already exist
    os.makedirs("repo", exist_ok=True)
    
    # Define the path where the repository will be cloned
    repo_path = "repo/"
    
    # Clone the specified GitHub repository into the local directory
    Repo.clone_from(repo_url, to_path=repo_path)


# Function to load Python files from a specified repository path as documents
def load_repo(repo_path):
    # Create a loader instance to read files from the given repository path
    loader = GenericLoader.from_filesystem(
        repo_path,               # The path to the repository containing the files
        glob="**/*",            # A glob pattern to match all files recursively in the directory
        suffixes=[".py"],       # Only include files with the .py suffix (Python files)
        parser=LanguageParser(   # Specify the parser for processing the files
            language=Language.PYTHON,  # Set the language for the parser to Python
            parser_threshold=500       # Set a threshold for the parser, possibly limiting processing for large files
        )
    )
    
    # Load the documents from the repository using the loader
    documents = loader.load()

    # Return the loaded documents
    return documents

# Function to create text chunks from a list of documents
def text_splitter(documents):
    # Initialize a text splitter to divide documents into chunks
    documents_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,  # Specify that the documents are in Python
        chunk_size=2000,           # Set the maximum size of each chunk to 2000 characters
        chunk_overlap=200          # Define the number of overlapping characters between consecutive chunks
    )
    
    # Split the input documents into smaller text chunks
    text_chunks = documents_splitter.split_documents(documents)

    # Return the resulting list of text chunks
    return text_chunks

# Function to load the OpenAI embeddings model
def load_embedding():
    # Initialize the embeddings model from OpenAI without any disallowed special tokens
    embeddings = OpenAIEmbeddings(disallowed_special=())
    
    # Return the initialized embeddings model
    return embeddings