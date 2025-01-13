
# Code With HTML and CSS Designing

import os
import time
import tempfile
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import google.generativeai as genai
from google.generativeai import upload_file, get_file

# Load environment variables and configure API
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def get_page_style() -> str:
    """Return the main page styling"""
    return """
    <style>

        /* Global styles */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }

        /* Button styling */
        .stButton button {
            background: linear-gradient(120deg, #4E65FF 0%, #92EFFD 100%);
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 10px;
            border: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }


        /* File uploader styling */
        [data-testid="stFileUploader"] {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            border: 2px dashed #4E65FF;
        }
        
        /* Text area styling */
        .stTextArea textarea {
            border-radius: 10px;
            border: 2px solid #4E65FF;
            padding: 1rem;
            font-size: 16px;
            height: 150px;
        }

        .app-container { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        .title-section { background: linear-gradient(120deg, #2E3192 0%, #1BFFFF 100%); padding: 2rem; border-radius: 15px; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; color: white; margin-bottom: 2rem; }
        .upload-section, .query-section, .welcome-section { 
            background: white; padding: 2rem; border-radius: 15px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0; 
        }
        .welcome-section { text-align: center; margin: 2rem 0; }
        .emoji-row { font-size: 3rem; margin: 1rem 0; }

        .subtitle {
            font-size: 1.2rem;
            margin-top: 1rem;
            opacity: 0.9;
        }
        /* Video container styling */
        .stVideo {
            max-width: 400px !important;
            margin: 0 auto !important;
            display: block !important;
        }
        .stVideo > video {
            aspect-ratio: 9/16 !important;
            width: 100% !important;
            height: auto !important;
            border-radius: 12px !important;
        }
        /* Fix video sizing in Streamlit */
        .element-container:has(>.stVideo) {
            max-width: 400px !important;
            margin: 0 auto !important;
        }

    </style>
    """

def render_header():
    """Render the app header"""
    st.markdown(f"""
    {get_page_style()}
    <div class="app-container">
        <div class="title-section">
            <h1>✨ Smart Video Analyzer</h1>
            <p class="subtitle">🤖 Powered by Advanced AI | 🎯 Precise Analysis | 🌐 Web Research</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def stream_analysis(response_placeholder, agent, prompt, video_file):
    """Stream the AI analysis response with proper markdown formatting"""
    response = agent.run(prompt, videos=[video_file])
    
    with st.spinner("🤖 AI is analyzing your video..."):
        # Since agent is configured with markdown=True, use markdown for response
        response_placeholder.markdown(response.content)

def main():
    st.set_page_config(page_title="✨ Smart Video Analyzer", page_icon="🎥", layout="wide")
    
    render_header()
    
    # Initialize AI agent with markdown enabled
    agent = Agent(
        name="Smart Video Analyzer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )
    
    # File upload section
    st.markdown("""
        <div class="upload-section">
            <h3>📤 Upload Your Video</h3>
            <style>
                .upload-section {
                    background: white;
                    padding: 2rem;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    margin: 1rem 0;
                }
            </style>
        </div>
    """, unsafe_allow_html=True)
    
    video_file = st.file_uploader(
        "Drop your video here ✨",
        type=['mp4', 'mov', 'avi'],
        help="Supporting MP4, MOV, and AVI formats"
    )
    
    if video_file:
        video_path = process_video_file(video_file)
        st.video(video_path)
        
        st.markdown("""
            <div class="query-section">
                <h3>🤔 What would you like to know?</h3>
            </div>
        """, unsafe_allow_html=True)
        
        query = st.text_area(
            "",
            placeholder="💭 Ask anything about the video... I'll analyze it in detail!",
            help="Be specific for better results",
            value="Please provide a comprehensive analysis of this video including key points, insights, and relevant web research result."
        )
        
        if st.button("🔮 Analyze Video", key="analyze_button"):
            if not query:
                st.warning("⚠️ Please enter your question first!")
            else:
                try:
                    with st.spinner("🎬 Processing your video..."):
                        processed_file = upload_file(video_path)
                        while processed_file.state.name == "PROCESSING":
                            time.sleep(1)
                            processed_file = get_file(processed_file.name)
                        
                        prompt = f"""
                        Provide a detailed analysis of this video addressing:
                        "{query}"
                        
                        Please structure your response in markdown format:
                        # 🎯 Main Points and Key Observations
                        
                        # 📊 Context and Insights
                        
                        # 💡 Web Research Findings
                        
                        Make it engaging and easy to understand.
                        """
                        
                        response_placeholder = st.empty()
                        stream_analysis(response_placeholder, agent, prompt, processed_file)
                
                except Exception as e:
                    st.error(f"❌ Oops! Something went wrong: {str(e)}")
                finally:
                    Path(video_path).unlink(missing_ok=True)
    else:
        st.markdown("""
            <div class="welcome-section">
                <h2>👋 Welcome to Smart Video Analyzer!</h2>
                <p>Upload a video to get started with AI-powered analysis</p>
                <p class="emoji-row">🎥 ✨ 🤖</p>
            </div>
        """, unsafe_allow_html=True)

def process_video_file(video_file) -> Optional[str]:
    """Process uploaded video file"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(video_file.read())
        return temp_file.name

if __name__ == "__main__":
    main()



# Code Without HTML and CSS Designing


# # import required libraries
# import os
# import time
# import tempfile
# from pathlib import Path
# from dotenv import load_dotenv
# import streamlit as st
# from phi.agent import Agent
# from phi.model.google import Gemini
# from phi.tools.duckduckgo import DuckDuckGo
# import google.generativeai as genai
# from google.generativeai import upload_file,get_file


# # Load environment variables from a .env file
# load_dotenv()

# # Set the GOOGLE_API_KEY from the environment variable
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# if GOOGLE_API_KEY:
#     genai.configure(api_key=GOOGLE_API_KEY)

# # Set Streamlit Page configuration
# st.set_page_config(
#     page_title="Multimodal AI Agent- Video Summarizer",
#     page_icon="🎥",
#     layout="wide"
# )

# st.title("Phidata Video AI Summarizer Agent 🎥🎤🖬")
# st.header("Powered by Gemini 2.0 Flash Exp")

# @st.cache_resource
# def initialize_ai_agent():

#     "Initialize the ai agent for the action"

#     return Agent(
#         name = "AI Video Summarizer Agent",
#         model = Gemini(id="gemini-2.0-flash-exp"),
#         tools = [DuckDuckGo],
#         markdown = True,
#     )

# # initialize the agent
# mr_video_summarizer = initialize_ai_agent()

# # File uploader option
# video_file_uploaded = st.file_uploader(
#     "Please Upload A Video File", type = ['mp4','mov','avi'], help = "Please Upload A Video File For AI Agent Video Analysis"
# )

# if video_file_uploaded:
#     with tempfile.NamedTemporaryFile(delete=False, suffix=" .mp4") as temporary_video:
#         temporary_video.write(video_file_uploaded.read())
#         video_file_uploaded_path = temporary_video.name

#     st.video(video_file_uploaded_path, format = "video/mp4", start_time = 0)

#     user_query = st.text_area(
#         "What Insights are You Seeking From the Video",
#         placeholder = "Ask Anything Abot the Video Content. This AI Agent will Analyze and Gather Additional Information or context if needed.",
#         help = "Please Provide Specific Questions or Insights you want from the Video",
#     )

#     if st.button("🔍 Analyze Video", key="analyze_video_button"):
#         if not user_query:
#             st.warning("Please Enter a Question Or Insight to Analyze the Video")
#         else:
#             try:
#                 with st.spinner("Processing Video and Gathering Insiights..."):

#                     # upload and process the video file
#                     processed_video_file = upload_file(video_file_uploaded_path)
#                     while processed_video_file.state.name == "PROCESSING":
#                         time.sleep(1)
#                         processed_video_file = get_file(processed_video_file.name)
                    
#                     # prompt generation for analysis
#                     video_analysis_prompt = (
#                         f"""
#                         Analyze the Uploaded Video For Content and Context.
#                         Respond to the Following Query using Video Insights and Supplementry Web Research:
#                         {user_query}
#                         Provide a Detailed, user-friendly, and an Actionable Response.
#                         """
#                     )

#                     # AI Agent Processing
#                     response = mr_video_summarizer.run(video_analysis_prompt, videos = [processed_video_file])
                
#                 # Display the analysis result
#                 st.subheader("Video Analysis Resut")
#                 st.markdown(response.content)
            
#             except Exception as error:
#                 st.error(f"An Error Occured during Viedo Analysis : {error}")
#             finally:

#                 # clean up temporary video file
#                 Path(video_file_uploaded_path).unlink(missing_ok = True)

# else:
#     st.info("Please Upload A Viedo File to Begin Analysis")
            

# # Customize text area height
# st.markdown(
#     """
#     <style>
#     .stTextArea textarea {
#         height: 100px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )