import os
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure page and styling with custom theme and icon
st.set_page_config(
    page_title="✨ MCQ Extractor Pro | AI-Powered Text Extraction",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/yourusername/mcq-extractor',
        'Report a bug': 'https://github.com/yourusername/mcq-extractor/issues',
        'About': '''
        ### MCQ Extractor Pro
        An AI-powered tool for extracting MCQs and text from images.
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
        <h1>📚 MCQ Extractor Pro 🤖</h1>
        <p style="font-size: 1.2rem; margin-top: 0.5rem;">
            Powered by Advanced AI Technology
        </p>
    </div>
""", unsafe_allow_html=True)

# Enhanced welcome message
st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h4>🎯 Welcome to MCQ Extractor Pro!</h4>
        <p>Transform your images into editable text with our advanced AI technology:</p>
        <ul>
            <li>🔍 Precise MCQ extraction</li>
            <li>📝 Maintains original formatting</li>
            <li>⚡ Fast and accurate processing</li>
            <li>💾 Easy export options</li>
        </ul>
    </div>
""", unsafe_allow_html=True)


# Enhanced welcome message
st.markdown("""
    <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
        <h4>💨 Please Upload An Image For MCQs Extraction Below 👇!</h4>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
        "📤 Drop your image here",
        type=["jpg", "jpeg", "png", "jfif"],
        help="Upload the image containing text such as MCQs or paragraphs."
    )

# Create two equal columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="stHeader"><h3>📂 Uploaded Image</h3></div>', unsafe_allow_html=True)
    
    # uploaded_file = st.file_uploader(
    #     "📤 Drop your image here",
    #     type=["jpg", "jpeg", "png", "jfif"],
    #     help="Upload the image containing text such as MCQs or paragraphs."
    # )

    if uploaded_file is not None:
        #st.markdown('<div class="uploadedImage">', unsafe_allow_html=True)
        image = Image.open(uploaded_file)
        st.image(image, caption='📸 Preview of uploaded image', use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    status_placeholder = st.empty()

    # Create the button and handle click logic
    extract_button = st.button("🔍 Extract Content ⚡", key="extract_button", help="Click to analyze the uploaded image and extract content.")


with col2:
    st.markdown('<div class="stHeader"><h3>📜 Extracted Content</h3></div>', unsafe_allow_html=True)
    
    default_prompt = """
    You are an expert in extracting text and questions from images. Given an image, identify and extract the content, 
    maintaining the format for any paragraphs or questions found. Do not specify correct answers.
    """

    content_placeholder = st.empty()
    button_placeholder = st.empty()

    if uploaded_file is not None and extract_button:
        try:
            with status_placeholder:
                st.info("🔄 Processing image... Please wait")
            
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(default_prompt, image_data, "Extract the content from the uploaded image.")
            
            st.balloons()
            status_placeholder.empty()
            
            content_placeholder.markdown(
                f'<div class="extractedContent"><pre>{response}</pre></div>',
                unsafe_allow_html=True
            )
            
            button_placeholder.download_button(
                label="📋 Download Extracted Content",
                data=response,
                file_name="extracted_content.md",
                mime="text/markdown",
                help="Click to download the extracted content as a markdown file"
            )

        except Exception as e:
            status_placeholder.error(f"🚫 Error: {str(e)}")

# Enhanced Footer
st.markdown("""
    <div class="footer">
        <h4>🚀 MCQ Extractor Pro</h4>
        <p>Made with ❤️ using Streamlit and Google's Gemini AI</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            💡 Pro Tip: For best results, ensure your image is clear and well-lit
        </p>
    </div>
""", unsafe_allow_html=True)

# import os
# from PIL import Image
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure page and styling with custom theme and icon
# st.set_page_config(
#     page_title="✨ MCQ Extractor Pro | AI-Powered Text Extraction",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="collapsed",
#     menu_items={
#         'Get Help': 'https://github.com/yourusername/mcq-extractor',
#         'Report a bug': 'https://github.com/yourusername/mcq-extractor/issues',
#         'About': '''
#         ### MCQ Extractor Pro
#         An AI-powered tool for extracting MCQs and text from images.
#         '''
#     }
# )

# st.markdown("""
#     <style>
#     /* Global Styles */
#     .main {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 2rem;
#     }
    
#     /* App Container */
#     .stApp {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#     }
    
#     /* Title Styling */
#     .stTitle {
#         background: linear-gradient(120deg, #2c3e50, #3498db);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white !important;
#         text-align: center;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#         margin-bottom: 2rem;
#     }
    
#     /* Header Styling */
#     .stHeader {
#         background: linear-gradient(120deg, #3498db, #2980b9);
#         padding: 1rem;
#         border-radius: 12px;
#         color: white !important;
#         margin-bottom: 1.5rem;
#         box-shadow: 0 4px 10px rgba(0,0,0,0.1);
#     }
    
#     /* Upload Section Styling */
#     .uploadedImage {
#         background: white;
#         border: 3px solid #3498db;
#         border-radius: 15px;
#         padding: 15px;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Enhanced Extract Button Styling */
#     div[data-testid="stButton"] button {
#         width: 100%;
#         min-height: 65px;
#         background: linear-gradient(45deg, #2ecc71, #27ae60);
#         color: white;
#         padding: 1rem 2.5rem;
#         border-radius: 12px;
#         font-size: 20px;
#         font-weight: bold;
#         border: none;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#         margin: 1rem 0;
#         letter-spacing: 1px;
#         line-height: 1.5;
#         text-transform: uppercase;
#     }
    
#     div[data-testid="stButton"] button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.15);
#         background: linear-gradient(45deg, #27ae60, #2ecc71);
#         letter-spacing: 2px;
#     }

#     div[data-testid="stButton"] button p {
#         font-size: 20px !important;
#     }

#     /* Extracted Content Styling */
#     .extractedContent {
#         background: white;
#         border-radius: 15px;
#         padding: 25px;
#         border: 3px solid #3498db;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Download Button Styling */
#     div[data-testid="stDownloadButton"] button {
#         background: linear-gradient(45deg, #9b59b6, #8e44ad);
#         color: white;
#         padding: 0.8rem 2rem;
#         border-radius: 8px;
#         font-weight: bold;
#         width: 100%;
#         border: none;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     div[data-testid="stDownloadButton"] button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.15);
#     }
    
#     /* Status Messages */
#     .stAlert {
#         border-radius: 10px;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Footer Styling */
#     .footer {
#         background: linear-gradient(120deg, #2c3e50, #3498db);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white;
#         text-align: center;
#         margin-top: 2rem;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Configure genai API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# def get_gemini_response(input, image, prompt):
#     response = model.generate_content([input, image[0], prompt])
#     return response.text

# def input_image_details(uploaded_file):
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()
#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No File Uploaded")

# # App Header with enhanced styling
# st.markdown("""
#     <div class="stTitle">
#         <h1>📚 MCQ Extractor Pro 🤖</h1>
#         <p style="font-size: 1.2rem; margin-top: 0.5rem;">
#             Powered by Advanced AI Technology
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # Enhanced welcome message
# st.markdown("""
#     <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
#         <h4>🎯 Welcome to MCQ Extractor Pro!</h4>
#         <p>Transform your images into editable text with our advanced AI technology:</p>
#         <ul>
#             <li>🔍 Precise MCQ extraction</li>
#             <li>📝 Maintains original formatting</li>
#             <li>⚡ Fast and accurate processing</li>
#             <li>💾 Easy export options</li>
#         </ul>
#     </div>
# """, unsafe_allow_html=True)

# # Create two equal columns
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown('<div class="stHeader"><h3>📂 Upload Section</h3></div>', unsafe_allow_html=True)
    
#     uploaded_file = st.file_uploader(
#         "📤 Drop your image here",
#         type=["jpg", "jpeg", "png", "jfif"],
#         help="Upload the image containing text such as MCQs or paragraphs."
#     )

#     if uploaded_file is not None:
#         st.markdown('<div class="uploadedImage">', unsafe_allow_html=True)
#         image = Image.open(uploaded_file)
#         st.image(image, caption='📸 Preview of uploaded image', use_container_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     status_placeholder = st.empty()

#     # Create the button and handle click logic
#     extract_button = st.button("🔍 Extract Content ⚡", key="extract_button", help="Click to analyze the uploaded image and extract content.")


# with col2:
#     st.markdown('<div class="stHeader"><h3>📜 Extracted Content</h3></div>', unsafe_allow_html=True)
    
#     default_prompt = """
#     You are an expert in extracting text and questions from images. Given an image, identify and extract the content, 
#     maintaining the format for any paragraphs or questions found. Do not specify correct answers.
#     """

#     content_placeholder = st.empty()
#     button_placeholder = st.empty()

#     if uploaded_file is not None and extract_button:
#         try:
#             with status_placeholder:
#                 st.info("🔄 Processing image... Please wait")
            
#             image_data = input_image_details(uploaded_file)
#             response = get_gemini_response(default_prompt, image_data, "Extract the content from the uploaded image.")
            
#             st.balloons()
#             status_placeholder.empty()
            
#             content_placeholder.markdown(
#                 f'<div class="extractedContent"><pre>{response}</pre></div>',
#                 unsafe_allow_html=True
#             )
            
#             button_placeholder.download_button(
#                 label="📋 Download Extracted Content",
#                 data=response,
#                 file_name="extracted_content.md",
#                 mime="text/markdown",
#                 help="Click to download the extracted content as a markdown file"
#             )

#         except Exception as e:
#             status_placeholder.error(f"🚫 Error: {str(e)}")

# # Enhanced Footer
# st.markdown("""
#     <div class="footer">
#         <h4>🚀 MCQ Extractor Pro</h4>
#         <p>Made with ❤️ using Streamlit and Google's Gemini AI</p>
#         <p style="font-size: 0.8rem; margin-top: 0.5rem;">
#             💡 Pro Tip: For best results, ensure your image is clear and well-lit
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# import os
# from PIL import Image
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure page and styling with custom theme and icon
# st.set_page_config(
#     page_title="✨ MCQ Extractor Pro | AI-Powered Text Extraction",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="collapsed",
#     menu_items={
#         'Get Help': 'https://github.com/yourusername/mcq-extractor',
#         'Report a bug': 'https://github.com/yourusername/mcq-extractor/issues',
#         'About': '''
#         ### MCQ Extractor Pro
#         An AI-powered tool for extracting MCQs and text from images.
#         '''
#     }
# )

# # Enhanced Custom CSS for styling
# st.markdown("""
#     <style>
#     /* Global Styles */
#     .main {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 2rem;
#     }
    
#     /* App Container */
#     .stApp {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#     }
    
#     /* Title Styling */
#     .stTitle {
#         background: linear-gradient(120deg, #2c3e50, #3498db);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white !important;
#         text-align: center;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#         margin-bottom: 2rem;
#     }
    
#     /* Header Styling */
#     .stHeader {
#         background: linear-gradient(120deg, #3498db, #2980b9);
#         padding: 1rem;
#         border-radius: 12px;
#         color: white !important;
#         margin-bottom: 1.5rem;
#         box-shadow: 0 4px 10px rgba(0,0,0,0.1);
#     }
    
#     /* Upload Section Styling */
#     .uploadedImage {
#         background: white;
#         border: 3px solid #3498db;
#         border-radius: 15px;
#         padding: 15px;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Updated Extract Button Styling */
#     .stButton > button {
#         width: 100%;
#         background: linear-gradient(45deg, #2ecc71, #27ae60);
#         color: white;
#         padding: 0.8rem 2rem;
#         border-radius: 8px;
#         font-weight: bold;
#         border: none;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.15);
#         background: linear-gradient(45deg, #27ae60, #2ecc71);
#     }

        

#     /* Extracted Content Styling */
#     .extractedContent {
#         background: white;
#         border-radius: 15px;
#         padding: 25px;
#         border: 3px solid #3498db;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Download Button Styling */
#     .stDownloadButton>button {
#         background: linear-gradient(45deg, #9b59b6, #8e44ad);
#         color: white;
#         padding: 0.8rem 2rem;
#         border-radius: 8px;
#         font-weight: bold;
#         width: 100%;
#         border: none;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     .stDownloadButton>button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.15);
#     }
    
#     /* Status Messages */
#     .stAlert {
#         border-radius: 10px;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Footer Styling */
#     .footer {
#         background: linear-gradient(120deg, #2c3e50, #3498db);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white;
#         text-align: center;
#         margin-top: 2rem;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
            
#     </style>
# """, unsafe_allow_html=True)

# # Configure genai API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# def get_gemini_response(input, image, prompt):
#     response = model.generate_content([input, image[0], prompt])
#     return response.text

# def input_image_details(uploaded_file):
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()
#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No File Uploaded")

# # App Header with enhanced styling
# st.markdown("""
#     <div class="stTitle">
#         <h1>📚 MCQ Extractor Pro 🤖</h1>
#         <p style="font-size: 1.2rem; margin-top: 0.5rem;">
#             Powered by Advanced AI Technology
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # Enhanced welcome message
# st.markdown("""
#     <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
#         <h4>🎯 Welcome to MCQ Extractor Pro!</h4>
#         <p>Transform your images into editable text with our advanced AI technology:</p>
#         <ul>
#             <li>🔍 Precise MCQ extraction</li>
#             <li>📝 Maintains original formatting</li>
#             <li>⚡ Fast and accurate processing</li>
#             <li>💾 Easy export options</li>
#         </ul>
#     </div>
# """, unsafe_allow_html=True)

# # Create two equal columns
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown('<div class="stHeader"><h3>📂 Upload Section</h3></div>', unsafe_allow_html=True)
    
#     uploaded_file = st.file_uploader(
#         "📤 Drop your image here",
#         type=["jpg", "jpeg", "png", "jfif"],
#         help="Upload the image containing text such as MCQs or paragraphs."
#     )

#     if uploaded_file is not None:
#         st.markdown('<div class="uploadedImage">', unsafe_allow_html=True)
#         image = Image.open(uploaded_file)
#         st.image(image, caption='📸 Preview of uploaded image', use_container_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     status_placeholder = st.empty()

#     # Create the button and handle click logic
#     extract_button = st.button("🔍 Extract Content ⚡", key="extract_button", help="Click to analyze the uploaded image and extract content.")


# with col2:
#     st.markdown('<div class="stHeader"><h3>📜 Extracted Content</h3></div>', unsafe_allow_html=True)
    
#     default_prompt = """
#     You are an expert in extracting text and questions from images. Given an image, identify and extract the content, 
#     maintaining the format for any paragraphs or questions found. Do not specify correct answers.
#     """

#     content_placeholder = st.empty()
#     button_placeholder = st.empty()

#     if uploaded_file is not None and extract_button:
#         try:
#             with status_placeholder:
#                 st.info("🔄 Processing image... Please wait")
            
#             image_data = input_image_details(uploaded_file)
#             response = get_gemini_response(default_prompt, image_data, "Extract the content from the uploaded image.")
            
#             st.balloons()
#             status_placeholder.empty()
            
#             content_placeholder.markdown(
#                 f'<div class="extractedContent"><pre>{response}</pre></div>',
#                 unsafe_allow_html=True
#             )
            
#             button_placeholder.download_button(
#                 label="📋 Download Extracted Content",
#                 data=response,
#                 file_name="extracted_content.md",
#                 mime="text/markdown",
#                 help="Click to download the extracted content as a markdown file"
#             )

#         except Exception as e:
#             status_placeholder.error(f"🚫 Error: {str(e)}")

# # Enhanced Footer
# st.markdown("""
#     <div class="footer">
#         <h4>🚀 MCQ Extractor Pro</h4>
#         <p>Made with ❤️ using Streamlit and Google's Gemini AI</p>
#         <p style="font-size: 0.8rem; margin-top: 0.5rem;">
#             💡 Pro Tip: For best results, ensure your image is clear and well-lit
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# import os
# from PIL import Image
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure page and styling with custom theme and icon
# st.set_page_config(
#     page_title="✨ MCQ Extractor Pro | AI-Powered Text Extraction",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="collapsed",
#     menu_items={
#         'Get Help': 'https://github.com/yourusername/mcq-extractor',
#         'Report a bug': 'https://github.com/yourusername/mcq-extractor/issues',
#         'About': '''
#         ### MCQ Extractor Pro
#         An AI-powered tool for extracting MCQs and text from images.
#         '''
#     }
# )

# # Enhanced Custom CSS for styling
# st.markdown("""
#     <style>
#     /* Global Styles */
#     .main {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 2rem;
#     }
    
#     /* App Container */
#     .stApp {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#     }
    
#     /* Title Styling */
#     .stTitle {
#         background: linear-gradient(120deg, #2c3e50, #3498db);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white !important;
#         text-align: center;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#         margin-bottom: 2rem;
#     }
    
#     /* Header Styling */
#     .stHeader {
#         background: linear-gradient(120deg, #3498db, #2980b9);
#         padding: 1rem;
#         border-radius: 12px;
#         color: white !important;
#         margin-bottom: 1.5rem;
#         box-shadow: 0 4px 10px rgba(0,0,0,0.1);
#     }
    
#     /* Extract Button Styling */
#     .extract-button {
#         background: linear-gradient(45deg, #2ecc71, #27ae60);
#         color: white;
#         padding: 0.8rem 2rem;
#         border-radius: 8px;
#         font-weight: bold;
#         width: 100%;
#         border: none;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     .extract-button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.15);
#         background: linear-gradient(45deg, #27ae60, #2ecc71);
#     }
    
#     /* Upload Section Styling */
#     .uploadedImage {
#         background: white;
#         border: 3px solid #3498db;
#         border-radius: 15px;
#         padding: 15px;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Extracted Content Styling */
#     .extractedContent {
#         background: white;
#         border-radius: 15px;
#         padding: 25px;
#         border: 3px solid #3498db;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Download Button Styling */
#     .stDownloadButton>button {
#         background: linear-gradient(45deg, #9b59b6, #8e44ad);
#         color: white;
#         padding: 0.8rem 2rem;
#         border-radius: 8px;
#         font-weight: bold;
#         width: 100%;
#         border: none;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     .stDownloadButton>button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.15);
#     }
    
#     /* Status Messages */
#     .stAlert {
#         border-radius: 10px;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
    
#     /* Footer Styling */
#     .footer {
#         background: linear-gradient(120deg, #2c3e50, #3498db);
#         padding: 1.5rem;
#         border-radius: 15px;
#         color: white;
#         text-align: center;
#         margin-top: 2rem;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Configure genai API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# def get_gemini_response(input, image, prompt):
#     response = model.generate_content([input, image[0], prompt])
#     return response.text

# def input_image_details(uploaded_file):
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()
#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No File Uploaded")

# # App Header with enhanced styling
# st.markdown("""
#     <div class="stTitle">
#         <h1>📚 MCQ Extractor Pro 🤖</h1>
#         <p style="font-size: 1.2rem; margin-top: 0.5rem;">
#             Powered by Advanced AI Technology
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# # Enhanced welcome message
# st.markdown("""
#     <div style='background: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
#         <h4>🎯 Welcome to MCQ Extractor Pro!</h4>
#         <p>Transform your images into editable text with our advanced AI technology:</p>
#         <ul>
#             <li>🔍 Precise MCQ extraction</li>
#             <li>📝 Maintains original formatting</li>
#             <li>⚡ Fast and accurate processing</li>
#             <li>💾 Easy export options</li>
#         </ul>
#     </div>
# """, unsafe_allow_html=True)

# # Create two equal columns
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown('<div class="stHeader"><h3>📂 Upload Section</h3></div>', unsafe_allow_html=True)
    
#     uploaded_file = st.file_uploader(
#         "📤 Drop your image here",
#         type=["jpg", "jpeg", "png", "jfif"],
#         help="Upload the image containing text such as MCQs or paragraphs."
#     )

#     if uploaded_file is not None:
#         st.markdown('<div class="uploadedImage">', unsafe_allow_html=True)
#         image = Image.open(uploaded_file)
#         st.image(image, caption='📸 Preview of uploaded image', use_container_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     status_placeholder = st.empty()
    
#     # Enhanced extract button
#     st.markdown("""
#         <button class="extract-button" id="extract-btn">
#             🔍 Extract Content 
#             <span style="font-size: 1.2em">⚡</span>
#         </button>
#     """, unsafe_allow_html=True)
#     extract_button = st.button("Extract Content", key="extract_button", help="Click to analyze the uploaded image and extract content.")

# with col2:
#     st.markdown('<div class="stHeader"><h3>📜 Extracted Content</h3></div>', unsafe_allow_html=True)
    
#     default_prompt = """
#     You are an expert in extracting text and questions from images. Given an image, identify and extract the content, 
#     maintaining the format for any paragraphs or questions found. Do not specify correct answers.
#     """

#     content_placeholder = st.empty()
#     button_placeholder = st.empty()

#     if uploaded_file is not None and extract_button:
#         try:
#             with status_placeholder:
#                 st.info("🔄 Processing image... Please wait")
            
#             image_data = input_image_details(uploaded_file)
#             response = get_gemini_response(default_prompt, image_data, "Extract the content from the uploaded image.")
            
#             st.balloons()
#             status_placeholder.empty()
            
#             content_placeholder.markdown(
#                 f'<div class="extractedContent"><pre>{response}</pre></div>',
#                 unsafe_allow_html=True
#             )
            
#             button_placeholder.download_button(
#                 label="📋 Download Extracted Content",
#                 data=response,
#                 file_name="extracted_content.md",
#                 mime="text/markdown",
#                 help="Click to download the extracted content as a markdown file"
#             )

#         except Exception as e:
#             status_placeholder.error(f"🚫 Error: {str(e)}")

# # Enhanced Footer
# st.markdown("""
#     <div class="footer">
#         <h4>🚀 MCQ Extractor Pro</h4>
#         <p>Made with ❤️ using Streamlit and Google's Gemini AI</p>
#         <p style="font-size: 0.8rem; margin-top: 0.5rem;">
#             💡 Pro Tip: For best results, ensure your image is clear and well-lit
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# import os
# from PIL import Image
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure page and styling
# st.set_page_config(
#     page_title="MCQ Extractor Pro",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS for styling
# st.markdown("""
#     <style>
#     .main {
#         padding: 2rem;
#     }
#     .stTitle {
#         background: linear-gradient(45deg, #3494e6, #ec6ead);
#         padding: 1rem;
#         border-radius: 10px;
#         color: white !important;
#         text-align: center;
#     }
#     .stHeader {
#         background: linear-gradient(45deg, #4b6cb7, #182848);
#         padding: 0.5rem;
#         border-radius: 8px;
#         color: white !important;
#         margin-bottom: 1rem;
#     }
#     .stButton>button {
#         background: linear-gradient(45deg, #3494e6, #ec6ead);
#         color: white;
#         border: none;
#         padding: 0.5rem 2rem;
#         border-radius: 5px;
#         font-weight: bold;
#         width: 100%;
#         transition: transform 0.2s;
#     }
#     .stButton>button:hover {
#         transform: translateY(-2px);
#     }
#     .uploadedImage {
#         border: 2px solid #4b6cb7;
#         border-radius: 10px;
#         padding: 10px;
#     }
#     .extractedContent {
#         background: #f8f9fa;
#         border-radius: 10px;
#         padding: 20px;
#         border: 2px solid #4b6cb7;
#     }
#     .stDownloadButton>button {
#         background: linear-gradient(45deg, #4b6cb7, #182848);
#         color: white;
#         border: none;
#         padding: 0.5rem 2rem;
#         border-radius: 5px;
#         font-weight: bold;
#         width: 100%;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Configure genai API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# def get_gemini_response(input, image, prompt):
#     response = model.generate_content([input, image[0], prompt])
#     return response.text

# def input_image_details(uploaded_file):
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()
#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No File Uploaded")

# # App Header with gradient background
# st.title("📄 MCQ Extractor Pro 🌟")

# # Add a brief description
# st.markdown("""
#     <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
#         <h4>Welcome to MCQ Extractor Pro!</h4>
#         <p>Upload an image containing text or MCQs, and let our AI extract the content for you. 
#         Supports various image formats including JPG, JPEG, PNG, and JFIF.</p>
#     </div>
# """, unsafe_allow_html=True)

# # Create two equal columns
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown('<div class="stHeader"><h3>📂 Upload Section</h3></div>', unsafe_allow_html=True)
    
#     # File uploader with custom styling
#     uploaded_file = st.file_uploader(
#         "",
#         type=["jpg", "jpeg", "png", "jfif"],
#         help="Upload the image containing text such as MCQs or paragraphs."
#     )

#     if uploaded_file is not None:
#         st.markdown('<div class="uploadedImage">', unsafe_allow_html=True)
#         image = Image.open(uploaded_file)
#         st.image(image, caption='📸 Uploaded Image', use_column_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     # Processing status indicator
#     status_placeholder = st.empty()
    
#     # Extract button with enhanced styling
#     extract_button = st.button(
#         "🔍 Extract Content",
#         help="Click to analyze the uploaded image and extract content.",
#         key="extract_button"
#     )

# with col2:
#     st.markdown('<div class="stHeader"><h3>📜 Extracted Content</h3></div>', unsafe_allow_html=True)
    
#     # Default prompt
#     default_prompt = """
#     You are an expert in extracting text and questions from images. Given an image, identify and extract the content, 
#     maintaining the format for any paragraphs or questions found. Do not specify correct answers.
#     """

#     # Content display area
#     content_placeholder = st.empty()
#     button_placeholder = st.empty()

#     if uploaded_file is not None and extract_button:
#         try:
#             with status_placeholder:
#                 st.info("🔄 Processing image... Please wait.")
            
#             image_data = input_image_details(uploaded_file)
#             response = get_gemini_response(default_prompt, image_data, "Extract the content from the uploaded image.")
            
#             # Success animation
#             st.balloons()
            
#             # Clear processing message
#             status_placeholder.empty()
            
#             # Display extracted content with styling
#             content_placeholder.markdown(
#                 f'<div class="extractedContent"><pre>{response}</pre></div>',
#                 unsafe_allow_html=True
#             )
            
#             # Copy button
#             button_placeholder.download_button(
#                 label="📋 Copy Extracted Content",
#                 data=response,
#                 file_name="extracted_content.md",
#                 mime="text/markdown"
#             )

#         except Exception as e:
#             status_placeholder.error(f"🚫 An error occurred: {str(e)}")

# # Footer
# st.markdown("""
#     <div style='text-align: center; margin-top: 2rem; padding: 1rem; background-color: #f0f2f6; border-radius: 10px;'>
#         <p>Made with ❤️ using Streamlit and Google's Gemini AI</p>
#     </div>
# """, unsafe_allow_html=True)

# # Importing Required Libraries
# import os
# from PIL import Image
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure genai API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Define a function to load gemini-1.5-flash model
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Define a function to get response from gemini model
# def get_gemini_response(input, image, prompt):
#     response = model.generate_content([input, image[0], prompt])
#     return response.text

# # For Image Setup
# def input_image_details(uploaded_file):
#     if uploaded_file is not None:
#         # Read the file into byte data
#         bytes_data = uploaded_file.getvalue()

#         image_parts = [
#             {
#                 "mime_type": uploaded_file.type,  # Get mime type of uploaded file
#                 "data": bytes_data
#             }
#         ]
#         return image_parts
#     else:
#         raise FileNotFoundError("No File Uploaded")

# # Streamlit Setup
# st.set_page_config(page_title="MCQ Extractor", layout="wide")

# # Main Header
# st.title("📄 MCQ Extractor from Image 🌟")

# # Layout Setup
# left_column, right_column = st.columns([1, 2])

# # File uploader header
# with left_column:
#     st.header("📂 Upload an Image with Text")
#     uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "jfif"], help="Upload the image containing text such as MCQs or paragraphs.")

#     # Display uploaded image
#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.image(image, caption='📸 Uploaded Image.', use_container_width=True)

#     # Submit button
#     extract_button = st.button("🔍 Extract Content", help="Click to analyze the uploaded image and extract content.")

# # Default prompt for the model
# default_prompt = """
# You are an expert in extracting text and questions from images. Given an image, identify and extract the content, maintaining the format for any paragraphs or questions found. Do not specify correct answers.
# """

# with right_column:
#     st.header("📜 Extracted Content:")
#     extracted_content = st.empty()
#     copy_button = st.empty()

# if uploaded_file is not None and extract_button:
#     try:
#         image_data = input_image_details(uploaded_file)
#         response = get_gemini_response(default_prompt, image_data, "Extract the content from the uploaded image.")

#         st.balloons()

#         # Display extracted content
#         extracted_content.markdown(f"```markdown\n{response}\n```")

#         # Add copy button for markdown
#         copy_button.download_button(
#             label="📋 Copy Extracted Content",
#             data=response,
#             file_name="extracted_content.md",
#             mime="text/markdown"
#         )

#     except Exception as e:
#         st.error(f"🚫 An error occurred: {str(e)}")
