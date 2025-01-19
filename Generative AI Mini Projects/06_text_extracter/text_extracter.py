import os
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure page and styling with custom theme and icon
st.set_page_config(
    page_title="✨ Text Images Extracter Buddy | AI-Powered Text Extraction",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/yourusername/text-extractor',
        'Report a bug': 'https://github.com/yourusername/text-extractor/issues',
        'About': '''
        ### Text Images Extracter Buddy
        An AI-powered tool for precise text extraction from images.
        '''
    }
)

st.markdown("""
    <style>
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
    }
    
    /* App Container */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Title Styling */
    .stTitle {
        background: linear-gradient(120deg, #2c3e50, #3498db);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Header Styling */
    .stHeader {
        background: linear-gradient(120deg, #3498db, #2980b9);
        padding: 1rem;
        border-radius: 12px;
        color: white !important;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Upload Section Styling */
    .uploadedImage {
        background: white;
        border: 3px solid #3498db;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Enhanced Extract Button Styling */
    div[data-testid="stButton"] button {
        width: 100%;
        min-height: 65px;
        background: linear-gradient(45deg, #2ecc71, #27ae60);
        color: white;
        padding: 1rem 2.5rem;
        border-radius: 12px;
        font-size: 20px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        letter-spacing: 1px;
        line-height: 1.5;
        text-transform: uppercase;
    }
    
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        background: linear-gradient(45deg, #27ae60, #2ecc71);
        letter-spacing: 2px;
    }

    div[data-testid="stButton"] button p {
        font-size: 20px !important;
    }

    /* Extracted Content Styling */
    .extractedContent {
        background: white;
        border-radius: 15px;
        padding: 25px;
        border: 3px solid #3498db;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Download Button Styling */
    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(45deg, #9b59b6, #8e44ad);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    div[data-testid="stDownloadButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Status Messages */
    .stAlert {
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Footer Styling */
    .footer {
        background: linear-gradient(120deg, #2c3e50, #3498db);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Configure genai API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# App Header with enhanced styling
st.markdown("""
    <div class="stTitle">
        <h1>📝 Text Images Extracter Buddy 🤖</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem;">
            Your Smart Companion for Text Extraction
        </p>
    </div>
""", unsafe_allow_html=True)

# Enhanced welcome message
st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h4>🎯 Welcome to Text Images Extracter Buddy!</h4>
        <p>Convert your images into perfectly formatted text with our intelligent AI:</p>
        <ul>
            <li>📊 Preserves original formatting and layout</li>
            <li>🎯 High accuracy text recognition</li>
            <li>⚡ Instant processing</li>
            <li>📥 Easy export functionality</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Upload instruction message
st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h4>💫 Upload Your Image Below For Text Extraction 👇!</h4>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
        "📤 Drop your image here",
        type=["jpg", "jpeg", "png", "jfif"],
        help="Upload any image containing text that you want to extract."
    )

# Create two equal columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="stHeader"><h3>📂 Uploaded Image</h3></div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='📸 Preview of uploaded image', use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    status_placeholder = st.empty()

    # Create the button and handle click logic
    extract_button = st.button("🔍 Extract Text ⚡", key="extract_button", help="Click to analyze the image and extract text content.")

with col2:
    st.markdown('<div class="stHeader"><h3>📜 Extracted Text</h3></div>', unsafe_allow_html=True)
    
    default_prompt = """
    You are an expert in extracting and formatting text from images. Please:
    1. Extract all text exactly as it appears in the image
    2. Maintain the original formatting, including:
       - Paragraphs and line breaks
       - Lists and bullet points
       - Indentation and spacing
       - Special characters and symbols
    3. Preserve any hierarchical structure in the text
    4. Keep the exact same text organization as shown in the image
    5. Do not add any additional formatting or interpretation
    6. Output the text in a clean, readable format
    """

    content_placeholder = st.empty()
    button_placeholder = st.empty()

    if uploaded_file is not None and extract_button:
        try:
            with status_placeholder:
                st.info("🔄 Processing image... Please wait")
            
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(default_prompt, image_data, "Extract and format the text exactly as it appears in the image.")
            
            st.balloons()
            status_placeholder.empty()
            
            content_placeholder.markdown(
                f'<div class="extractedContent"><pre>{response}</pre></div>',
                unsafe_allow_html=True
            )
            
            button_placeholder.download_button(
                label="📋 Download Extracted Text",
                data=response,
                file_name="extracted_text.md",
                mime="text/markdown",
                help="Click to download the extracted text as a markdown file"
            )

        except Exception as e:
            status_placeholder.error(f"🚫 Error: {str(e)}")

# Enhanced Footer
st.markdown("""
    <div class="footer">
        <h4>🚀 Text Images Extracter Buddy</h4>
        <p>Made with ❤️ using Streamlit and Google's Gemini AI</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            💡 Pro Tip: For best results, use clear images with good lighting and resolution
        </p>
    </div>
""", unsafe_allow_html=True)