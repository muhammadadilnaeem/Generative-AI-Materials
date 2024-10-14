
# Import libraries
import os
from dotenv import load_dotenv
from src.prompt import *
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Set Up OpenAI API Key
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Set up a File Processing Function
def file_processing(file_path):
    # Load data from a PDF file using the specified file path
    loader = PyPDFLoader(file_path)  # Initialize the PDF loader with the given file path
    data = loader.load()              # Load the content of the PDF into a data structure

    question_gen = ''                 # Initialize an empty string to hold the concatenated page content

    # Iterate through each page in the loaded PDF data
    for page in data:
        question_gen += page.page_content  # Append the content of each page to the question_gen string
        
    # Initialize a TokenTextSplitter for chunking the question generation text
    splitter_ques_gen = TokenTextSplitter(
        model_name='gpt-3.5-turbo',  # Specify the language model to use for tokenization
        chunk_size=10000,            # Set the maximum size of each text chunk to 10,000 tokens
        chunk_overlap=200            # Allow an overlap of 200 tokens between consecutive chunks
    )

    # Split the concatenated question text into manageable chunks
    chunks_ques_gen = splitter_ques_gen.split_text(question_gen)

    # Create a list of Document objects from the text chunks for question generation
    document_ques_gen = [Document(page_content=t) for t in chunks_ques_gen]

    # Initialize another TokenTextSplitter for chunking the answers from the questions
    splitter_ans_gen = TokenTextSplitter(
        model_name='gpt-3.5-turbo',  # Specify the language model to use for tokenization
        chunk_size=1000,              # Set the maximum size of each text chunk to 1,000 tokens
        chunk_overlap=100             # Allow an overlap of 100 tokens between consecutive chunks
    )

    # Split the list of question documents into smaller segments for answer generation
    document_answer_gen = splitter_ans_gen.split_documents(document_ques_gen)

    # Return the lists of question and answer documents
    return document_ques_gen, document_answer_gen

# Set up a LLM Pipeline Function
def llm_pipeline(file_path):
    # Process the input PDF file to generate question and answer documents
    document_ques_gen, document_answer_gen = file_processing(file_path)

    # Initialize the language model pipeline for question generation
    llm_ques_gen_pipeline = ChatOpenAI(
        temperature=0.3,               # Set the randomness of the output for more creative responses
        model="gpt-3.5-turbo"          # Specify the model to use for generating questions
    )

    # Create a prompt template for generating questions
    PROMPT_QUESTIONS = PromptTemplate(
        template=prompt_template,       # Use the previously defined prompt template
        input_variables=["text"]        # Specify the input variable for the template
    )

    # Create a prompt template for refining questions
    REFINE_PROMPT_QUESTIONS = PromptTemplate(
        input_variables=["existing_answer", "text"],  # Specify input variables for refining
        template=refine_template,                      # Use the previously defined refine template
    )

    # Load the summarization chain for generating and refining questions
    ques_gen_chain = load_summarize_chain(
        llm=llm_ques_gen_pipeline,                   # Specify the language model for question generation
        chain_type="refine",                          # Set the type of chain to "refine"
        verbose=True,                                 # Enable detailed logging during execution
        question_prompt=PROMPT_QUESTIONS,            # Use the prompt template for generating questions
        refine_prompt=REFINE_PROMPT_QUESTIONS         # Use the prompt template for refining questions
    )

    # Run the question generation chain on the document containing questions
    ques = ques_gen_chain.run(document_ques_gen)

    # Initialize embeddings for document retrieval
    embeddings = OpenAIEmbeddings()

    # Create a FAISS vector store from the answer documents using the embeddings
    vector_store = FAISS.from_documents(document_answer_gen, embeddings)

    # Initialize the language model for generating answers
    llm_answer_gen = ChatOpenAI(
        temperature=0.1,                # Set a lower randomness for more predictable answers
        model="gpt-3.5-turbo"           # Specify the model to use for generating answers
    )

    # Split the generated questions into a list
    ques_list = ques.split("\n")
    
    # Filter the list to include only valid questions (ending with '?' or '.')
    filtered_ques_list = [element for element in ques_list if element.endswith('?') or element.endswith('.')]

    # Create a RetrievalQA chain for answering questions using the vector store
    answer_generation_chain = RetrievalQA.from_chain_type(
        llm=llm_answer_gen,              # Specify the language model for generating answers
        chain_type="stuff",              # Set the type of chain to "stuff" for simple retrieval
        retriever=vector_store.as_retriever()  # Use the FAISS vector store as the retriever
    )

    # Return the answer generation chain and the filtered list of questions
    return answer_generation_chain, filtered_ques_list