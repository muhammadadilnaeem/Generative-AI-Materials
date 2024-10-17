
# Import Libraries
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# Load pdf data
def load_pdf_file(directory_path):
    # Create a DirectoryLoader instance to load PDF files from the specified directory.
    loader = DirectoryLoader(directory_path, 
                             glob="*.pdf",  # Specify that we want to load files with a .pdf extension
                             loader_cls=PyPDFLoader)  # Use PyPDFLoader to handle the loading of PDF files
    
    # Load the documents (PDF files) using the loader
    documents = loader.load()
    
    # Return the loaded documents
    return documents


# Split data into chunks
def text_split(extracted_data):
    # Create an instance of RecursiveCharacterTextSplitter to split text into manageable chunks.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,    # Set the maximum size of each chunk to 500 characters
        chunk_overlap=20,   # Allow an overlap of 20 characters between consecutive chunks
    )
    # Split the extracted data into text chunks using the defined splitter
    text_chunks = text_splitter.split_documents(extracted_data)
    
    # Return the list of text chunks
    return text_chunks

# Download embedding model
def download_huggingface_embedding():
    # Create an instance of the updated HuggingFaceEmbeddings class.
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding