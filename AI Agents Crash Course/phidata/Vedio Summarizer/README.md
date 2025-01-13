
---

# **Smart Video Analyzer**

Smart Video Analyzer is a web-based application powered by advanced AI technologies. It allows users to upload videos and receive detailed analyses, including key points, insights, and relevant web research findings. The application uses an intuitive interface with elegant HTML and CSS design for a seamless user experience.

---

![alt text](<vedio summrizer by phidata.png>)

---

## **Features**

- **AI-Powered Analysis**: Leverages cutting-edge AI models to analyze video content.
- **Web Research Integration**: Provides insights backed by web research using DuckDuckGo.
- **User-Friendly Interface**: Styled with custom HTML and CSS for an engaging user experience.
- **Markdown-Based Output**: Generates structured and easy-to-read results.
- **Multiple Video Formats Supported**: Accepts MP4, MOV, and AVI formats.

---

## **Technologies Used**

- **Python**: Backend scripting and logic.
- **Streamlit**: For creating the web application interface.
- **Phi**: Integrates AI agent capabilities.
  - [Gemini Model](https://phi-model.google): Advanced AI model for content analysis.
  - [DuckDuckGo Tool](https://duckduckgo.com): Fetches web-based research insights.
- **Google Generative AI API**: Processes and analyzes video files.
- **HTML & CSS**: Custom styling for an enhanced user experience.
- **Tempfile**: Handles temporary storage of uploaded files.

---

## **Installation**

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Set Up Environment**:
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Create a `.env` file in the root directory and add your Google API key:
     ```env
     GOOGLE_API_KEY=your_google_api_key
     ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

4. **Access the App**:
   Open your browser and navigate to `http://localhost:8501`.

---

## **How to Use**

1. **Upload Your Video**:
   - Click the "Upload Your Video" section.
   - Drop or select your video file (MP4, MOV, AVI).

2. **Ask a Question**:
   - Enter your query in the provided text area.
   - Example: "What are the key points and insights in this video?"

3. **Analyze the Video**:
   - Click the "Analyze Video" button.
   - Wait while the AI processes your video and generates results.

4. **View Results**:
   - AI-generated analysis, structured in markdown format, will appear on the screen.

---

## **Project Structure**

```
├── app.py               # Main application script
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .env                 # Environment variables (ignored in version control)
```

---

## **Custom Styling**

The application incorporates custom HTML and CSS to enhance the visual experience. Styles include:

- **Gradient Backgrounds**
- **Hover Effects**
- **Customized Buttons**
- **File Uploader Design**

---

## **Known Issues and Limitations**

- Processing time may vary based on video size and complexity.
- Requires a valid Google API key for proper functionality.
- Currently supports only MP4, MOV, and AVI formats.

---

## **Future Enhancements**

- Add support for more video formats.
- Provide multilingual analysis capabilities.
- Integrate more AI models for specialized analyses.
- Enhance video preview capabilities.

---

## **Acknowledgments**

- [Streamlit](https://streamlit.io) for their easy-to-use framework.
- [Phi Framework](https://phi-model.google) for AI integration.
- [DuckDuckGo](https://duckduckgo.com) for web research capabilities.
- Google Generative AI for video processing.

-----------