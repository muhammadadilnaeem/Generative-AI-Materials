
# In case you increase or update data

import os
from src.helper import load_pdf_file, download_huggingface_embedding, text_split
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# Set up pinecone
load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")

# Load data
extracted_data = load_pdf_file(data="data/")

# Split data into chunks
text_chunks = text_split(extracted_data)

# download embedding model
embedding = download_huggingface_embedding()

# Initialize pinecone
# Define the name of the index to be used for the Pinecone vector database.
index_name = "medical-chatbot-implementation"

# Initialize a Pinecone client using the provided API key.
pc = Pinecone(api_key=api_key)

# Check if the specified index already exists in the Pinecone environment.
if index_name not in pc.list_indexes().names():
    # If the index does not exist, create a new index with the specified parameters.
    pc.create_index(
        name=index_name,            # Set the name of the index
        dimension=384,              # Specify the dimensionality of the vectors stored in the index
        metric="cosine",            # Use cosine similarity as the distance metric
        spec=ServerlessSpec(        # Define the serverless specification for the index
            cloud="aws",            # Specify the cloud provider
            region="us-east-1"      # Specify the region for the index
        )
    )

# Create a PineconeVectorStore instance from the provided documents and embedding model.
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,  # The list of text chunks to be stored in the vector store.
    index_name=index_name,  # The name of the index where the vectors will be stored.
    embedding=embedding,     # The embedding model used to convert documents into vector representations.
)