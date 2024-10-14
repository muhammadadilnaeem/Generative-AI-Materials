# Import libraries
import os
import csv
import json
import uvicorn
import aiofiles
from fastapi import FastAPI, Form, Request, Response, File, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from src.helper import llm_pipeline

# Create an instance of the FastAPI application
app = FastAPI()

# Mount a static file directory to serve static files from the "static" folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates for rendering HTML files from the "templates" directory
templates = Jinja2Templates(directory="templates")

# Define a GET endpoint for the root URL ("/")
@app.get("/")
async def index(request: Request):
    # Render the "index.html" template and pass the request object to it
    return templates.TemplateResponse("index.html", {"request": request})

# Define a POST endpoint for uploading a PDF file
@app.post("/upload")
async def chat(request: Request, pdf_file: bytes = File(), filename: str = Form(...)):
    # Set the base folder where the uploaded PDF files will be stored
    base_folder = 'static/docs/'
    
    # Check if the base folder exists; if not, create it
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
        
    # Construct the full path for the uploaded PDF file
    pdf_filename = os.path.join(base_folder, filename)

    # Asynchronously open the file in write-binary mode and save the uploaded content
    async with aiofiles.open(pdf_filename, 'wb') as f:
        await f.write(pdf_file)  # Write the uploaded file bytes to the specified path

    # Prepare a JSON response indicating success and the filename of the uploaded PDF
    response_data = jsonable_encoder(json.dumps({"msg": 'success', "pdf_filename": pdf_filename}))
    
    # Create a Response object with the JSON data
    res = Response(response_data)
    
    # Return the response to the client
    return res

# Define a POST endpoint for generating CSV files
def get_csv(file_path):
    # Generate the answer generation chain and question list by processing the input file
    answer_generation_chain, ques_list = llm_pipeline(file_path)
    
    # Set the base folder where the output CSV file will be stored
    base_folder = 'static/output/'
    
    # Check if the base folder exists; if not, create it
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    
    # Construct the full path for the output CSV file
    output_file = base_folder + "QA.csv"
    
    # Open the CSV file for writing, with UTF-8 encoding
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)  # Create a CSV writer object
        
        # Write the header row to the CSV file
        csv_writer.writerow(["Question", "Answer"])  

        # Iterate through each question in the question list
        for question in ques_list:
            print("Question: ", question)  # Print the current question
            answer = answer_generation_chain.run(question)  # Generate an answer for the current question
            print("Answer: ", answer)  # Print the generated answer
            print("--------------------------------------------------\n\n")  # Print a separator for readability

            # Save the question and answer to the CSV file
            csv_writer.writerow([question, answer])
    
    # Return the path of the output CSV file
    return output_file

# Define a POST endpoint for analyzing a PDF file
@app.post("/analyze")
async def chat(request: Request, pdf_filename: str = Form(...)):
    # Call the get_csv function to process the PDF file and generate a CSV output
    output_file = get_csv(pdf_filename)

    # Prepare a JSON response containing the path of the output CSV file
    response_data = jsonable_encoder(json.dumps({"output_file": output_file}))
    
    # Create a Response object with the JSON data
    res = Response(response_data)
    
    # Return the response to the client
    return res

# Run the application using Uvicorn if this script is executed directly
if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8080, reload=True)  # Start the server on host 0.0.0.0 and port 8080 with auto-reload

# type this in bowser to see result    (  http://127.0.0.1:8080/  )