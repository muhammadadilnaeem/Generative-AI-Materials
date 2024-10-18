
---

# **GitHub Source Code Analyzer**

Welcome to the **GitHub Source Code Analyzer** project! This web application allows users to analyze Python code from a GitHub repository by extracting and embedding the code into a vector database. The tool leverages OpenAI's embedding models and Chroma's vector database to enable users to ask questions about the code and receive detailed, context-aware responses.

## **Features**

- **Extract Python Code**: The app extracts Python files from a GitHub repository provided by the user.
- **Create Embeddings**: The Python code is processed to create embeddings using OpenAI's embedding model.
- **Store in Chroma Vector Database**: The embeddings are stored in a vector database for fast and efficient querying.
- **Natural Language Queries**: Users can ask natural language questions about the code, and the system will return responses based on the embedded code snippets.

## **How It Works**

1. **Input the GitHub URL**: Users provide the URL of a GitHub repository containing Python files.
2. **Code Processing**: The application extracts the Python files, generates embeddings for the code, and stores them in a Chroma vector database.
3. **Ask Questions**: Once the processing is complete, users can ask questions about the Python code, and the application will generate a response based on the code's structure and logic.
4. **Response Generation**: The app uses OpenAI models to generate natural language responses from the embeddings stored for the given repository.

## **Technology Stack**

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **API**: OpenAI API (for embeddings and text generation)
- **Database**: Chroma (Vector Database for embeddings)

## **Project Demo**


https://github.com/user-attachments/assets/7d10fc43-7cc9-4df7-9ab8-13b393e9e6a1


## **Getting Started**

### **Prerequisites**

To run this project locally, you need to have the following installed:

- Python 3.x
- OpenAI API Key (You can get this by signing up at [OpenAI](https://platform.openai.com/signup))
- Git

### **Installation**

1. **Clone the repository**:
    ```bash
    git clone https://github.com/muhammadadilnaeem/Generative-AI-Materials.git
    cd Generative-AI-Materials/Langchain/Interview_question_creater_web_app
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the root directory and add your OpenAI API key:
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Run the application**:
    ```bash
    python app.py
    ```

6. Open your browser and navigate to `http://localhost:5000` to access the app.

## **Usage**

### **Step-by-step guide:**

1. **Enter the GitHub URL**: Copy and paste the URL of the GitHub repository containing Python files into the input field.
2. **Hit the Send Button**: Click the **"Send"** button to start processing.
3. **Wait for Embeddings to Be Generated**: A message will appear saying, **"Please wait, your data is being processed."** This may take a moment as the system extracts Python files and generates embeddings.
4. **Ask a Question**: After processing is complete, you will see the message, **"Processing complete. Now you can ask a question."** Type in your question about the code.
5. **Receive Detailed Responses**: The application will use the stored embeddings and the OpenAI model to generate and return a detailed response based on the Python code from the repository.

## **Example**

1. **Input**: A GitHub repository URL (e.g., `https://github.com/someuser/somerepo`)
2. **Query**: *"What does the `calculate_total()` function do?"*
3. **Response**: A detailed explanation of the function extracted from the code, describing the logic, input parameters, and output.

## **Project Structure**

```bash
├── app.py               # Main Flask app
├── templates/
│   └── index.html       # Frontend HTML
├── static/
│   ├── css/             # CSS files for styling
│   ├── js/              # JavaScript files
├── requirements.txt     # Project dependencies
└── README.md            # Project README
```

## **Future Improvements**

- Add support for additional programming languages besides Python.
- Implement better error handling for edge cases, such as when repositories don’t contain Python files.
- Optimize the embedding process for larger repositories with many files.


## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

**Thank you for checking out GitHub Source Code Analyzer!**  
If you have any questions or feedback, feel free to reach out or submit an issue on GitHub.

------

