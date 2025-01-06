
# import required libraries
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

def load_custom_css():
    """Load custom CSS for enhanced UI"""
    st.markdown("""
        <style>
        /* Global styles */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Gradient title background */
        .title-gradient {
            background: linear-gradient(120deg, #2E3192 0%, #1BFFFF 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        
        /* Card container styles */
        .card-container {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        /* Analysis results styling */
        .analysis-header {
            background: linear-gradient(120deg, #4E65FF 0%, #92EFFD 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
        }
        
        .analysis-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 5px solid #4E65FF;
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
        
        /* Custom point styling */
        .point-container {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #4E65FF;
            transition: all 0.3s ease;
        }
        
        .point-container:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* Spinner styling */
        .loading-spinner {
            text-align: center;
            padding: 2rem;
            color: #4E65FF;
        }
        </style>
    """, unsafe_allow_html=True)

def format_analysis_response(content: str) -> str:
    """Format the analysis response with better styling and structure"""
    sections = content.split('📊 Relevant context and insights')
    main_points = sections[0].replace('🎯 Main points and key observations', '')
    
    formatted_response = f"""
    <div class="analysis-section">
        <h3>🎯 Key Observations</h3>
        {main_points}
    </div>
    """
    
    if len(sections) > 1:
        insights = sections[1].split('💡 Additional information')[0]
        formatted_response += f"""
        <div class="analysis-section">
            <h3>📊 Context & Insights</h3>
            {insights}
        </div>
        """
        
        web_research = sections[1].split('💡 Additional information')[1]
        formatted_response += f"""
        <div class="analysis-section">
            <h3>💡 Web Research Findings</h3>
            {web_research}
        </div>
        """
    
    return formatted_response

def stream_analysis(response_placeholder, agent, prompt, video_file):
    """Stream the AI analysis response with enhanced formatting"""
    response = agent.run(prompt, videos=[video_file])
    content = response.content
    
    # Create loading animation
    with st.spinner("🤖 AI is analyzing your video..."):
        formatted_response = format_analysis_response(content)
        response_placeholder.markdown(formatted_response, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="✨ Smart Video Analyzer", page_icon="🎥", layout="wide")
    load_custom_css()
    
    # Title section with gradient background
    st.markdown("""
        <div class="title-gradient">
            <h1>✨ Smart Video Analyzer</h1>
            <p style="font-size: 1.2rem;">🤖 Powered by Advanced AI | 🎯 Precise Analysis | 🌐 Web Research</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize AI agent
    agent = create_agent()
    
    # File upload section
    st.markdown("""
        <div class="card-container">
            <h3>📤 Upload Your Video</h3>
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
            <div class="card-container">
                <h3>🤔 What would you like to know?</h3>
            </div>
        """, unsafe_allow_html=True)
        
        query = st.text_area(
            "",
            placeholder="💭 Ask anything about the video... I'll analyze it in detail!",
            help="Be specific for better results",
            value="Please provide a comprehensive analysis of this video including key points, insights, and relevant web research."
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
                        
                        Structure your response with:
                        🎯 Main points and key observations
                        📊 Relevant context and insights
                        💡 Additional information from web research
                        
                        Make it engaging and easy to understand.
                        """
                        
                        st.markdown("""
                            <div class="analysis-header">
                                <h2>✨ Analysis Results</h2>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        response_placeholder = st.empty()
                        stream_analysis(response_placeholder, agent, prompt, processed_file)
                
                except Exception as e:
                    st.error(f"❌ Oops! Something went wrong: {str(e)}")
                finally:
                    Path(video_path).unlink(missing_ok=True)
    else:
        st.markdown("""
            <div class="card-container" style="text-align: center;">
                <h2>👋 Welcome to Smart Video Analyzer!</h2>
                <p>Upload a video to get started with AI-powered analysis</p>
                <p style="font-size: 3rem;">🎥 ✨ 🤖</p>
            </div>
        """, unsafe_allow_html=True)

def create_agent() -> Agent:
    """Initialize AI agent with proper configuration"""
    return Agent(
        name="Smart Video Analyzer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

def process_video_file(video_file) -> Optional[str]:
    """Process uploaded video file"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        temp_file.write(video_file.read())
        return temp_file.name

if __name__ == "__main__":
    main()

# # import required libraries
# import os
# import time
# import tempfile
# from pathlib import Path
# from typing import Optional
# from dotenv import load_dotenv
# import streamlit as st
# from phi.agent import Agent
# from phi.model.google import Gemini
# from phi.tools.duckduckgo import DuckDuckGo
# import google.generativeai as genai
# from google.generativeai import upload_file, get_file

# # Load environment variables and configure API
# load_dotenv()
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# if GOOGLE_API_KEY:
#     genai.configure(api_key=GOOGLE_API_KEY)

# # Custom CSS for better UI
# def load_custom_css():
#     st.markdown("""
#         <style>
#         /* Main container styling */
#         .main {
#             padding: 2rem;
#         }
        
#         /* Header styling */
#         .title-container {
#             background-color: #f0f2f6;
#             padding: 2rem;
#             border-radius: 10px;
#             margin-bottom: 2rem;
#         }
        
#         /* File uploader styling */
#         .uploadedFile {
#             background-color: #ffffff;
#             border: 2px dashed #cccccc;
#             border-radius: 10px;
#             padding: 1rem;
#         }
        
#         /* Text area customization */
#         .stTextArea textarea {
#             height: 120px;
#             font-size: 16px;
#             border-radius: 8px;
#         }
        
#         /* Button styling */
#         .stButton button {
#             width: 100%;
#             padding: 0.75rem;
#             background-color: #FF4B4B;
#             color: white;
#             border-radius: 8px;
#             transition: all 0.3s;
#         }
        
#         .stButton button:hover {
#             background-color: #FF2E2E;
#             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         }
        
#         /* Analysis result container */
#         .analysis-container {
#             background-color: #ffffff;
#             padding: 1.5rem;
#             border-radius: 10px;
#             box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
#             margin-top: 2rem;
#         }
#         </style>
#     """, unsafe_allow_html=True)

# def create_agent() -> Agent:
#     """
#     Initialize and return the AI agent with proper configuration.
#     Fixes the DuckDuckGo warning by properly instantiating the tool.
#     """
#     return Agent(
#         name="AI Video Summarizer Agent",
#         model=Gemini(id="gemini-2.0-flash-exp"),
#         tools=[DuckDuckGo()],  # Instantiate the class instead of passing the class itself
#         markdown=True,
#     )

# def process_video_file(video_file) -> Optional[str]:
#     """
#     Process the uploaded video file and return the temporary file path.
#     """
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
#         temp_file.write(video_file.read())
#         return temp_file.name

# def stream_analysis(response_placeholder, agent, prompt, video_file):
#     """
#     Stream the AI analysis response with a typewriter effect.
#     """
#     response = agent.run(prompt, videos=[video_file])
#     content = response.content
    
#     # Simulate streaming effect
#     full_response = ""
#     for chunk in content.split():
#         full_response += chunk + " "
#         response_placeholder.markdown(full_response + "▌")
#         time.sleep(0.05)
    
#     response_placeholder.markdown(full_response)

# def main():
#     # Page configuration
#     st.set_page_config(
#         page_title="🎥 Advanced Video Summarizer",
#         page_icon="🎥",
#         layout="wide"
#     )
    
#     # Load custom CSS
#     load_custom_css()
    
#     # Title section with emojis
#     st.markdown("""
#         <div class="title-container">
#             <h1>🎥 Professional Video AI Summarizer</h1>
#             <h3>🤖 Powered by Gemini 2.0 Flash Exp | 🔍 Advanced Analysis</h3>
#         </div>
#     """, unsafe_allow_html=True)
    
#     # Initialize AI agent
#     agent = create_agent()
    
#     # File upload section
#     st.markdown("### 📤 Upload Your Video")
#     video_file = st.file_uploader(
#         "Choose a video file",
#         type=['mp4', 'mov', 'avi'],
#         help="Upload a video file for AI analysis (MP4, MOV, or AVI format)"
#     )
    
#     if video_file:
#         # Process video file
#         video_path = process_video_file(video_file)
        
#         # Display video
#         st.video(video_path, format="video/mp4", start_time=0)
        
#         # Query input
#         st.markdown("### 💭 What would you like to know about the video?")
#         query = st.text_area(
#             "",
#             placeholder="Ask anything about the video content. Our AI will analyze and provide detailed insights.",
#             help="Be specific in your questions for better analysis results",
#             value="Please summarize the uploaded video, list the key points, and also search the web for information about the topic mentioned in the video.",
#         )
        
#         # Analysis button
#         if st.button("🔍 Analyze Video", key="analyze_button"):
#             if not query:
#                 st.warning("⚠️ Please enter a question or analysis prompt")
#             else:
#                 try:
#                     with st.spinner("🔄 Processing video and gathering insights..."):
#                         # Process video file
#                         processed_file = upload_file(video_path)
#                         while processed_file.state.name == "PROCESSING":
#                             time.sleep(1)
#                             processed_file = get_file(processed_file.name)
                        
#                         # Generate analysis prompt
#                         prompt = f"""
#                         Analyze this video in detail and address the following query:
#                         "{query}"
                        
#                         Please provide:
#                         🎯 Main points and key observations
#                         📊 Relevant context and insights
#                         💡 Additional information from web research
                        
#                         Make the response detailed yet easy to understand.
#                         """
                        
#                         # Create placeholder for streaming response
#                         st.markdown("### 📝 Analysis Results")
#                         response_placeholder = st.empty()
                        
#                         # Stream the analysis
#                         stream_analysis(response_placeholder, agent, prompt, processed_file)
                
#                 except Exception as e:
#                     st.error(f"❌ Error during analysis: {str(e)}")
#                 finally:
#                     # Cleanup
#                     Path(video_path).unlink(missing_ok=True)
#     else:
#         # Display welcome message
#         st.info("👋 Welcome! Please upload a video file to begin analysis")

# if __name__ == "__main__":
#     main()




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