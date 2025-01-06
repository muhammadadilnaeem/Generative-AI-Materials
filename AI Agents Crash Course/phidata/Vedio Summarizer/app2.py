
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
    """Load custom CSS styles"""
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(120deg, #2E3192 0%, #1BFFFF 100%);
            color: white !important;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        .main-header h1 {
            color: white !important;
            margin: 0;
            padding: 0;
        }
        
        .analysis-section {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 5px solid #4E65FF;
        }
        
        .analysis-section h3 {
            color: #2E3192;
            margin-bottom: 15px;
        }
        
        .step-list {
            margin-left: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def format_analysis(content: str) -> str:
    """Format the analysis content for better display"""
    # Split content into sections
    sections = content.split('\n')
    formatted_sections = []
    current_section = ""
    
    for line in sections:
        line = line.strip()
        if line.startswith('**') and '**' in line[2:]:
            # Handle section headers
            if current_section:
                formatted_sections.append(current_section)
            current_section = f"### {line.strip('*')}\n"
        elif line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
            # Handle numbered lists
            current_section += f"{line}\n"
        elif line:
            # Handle regular content
            current_section += f"{line}\n"
    
    if current_section:
        formatted_sections.append(current_section)
    
    return "\n".join(formatted_sections)

def stream_analysis(response_placeholder, agent, prompt, video_file):
    """Stream the analysis with proper formatting"""
    with st.spinner("🎬 Analyzing your video..."):
        response = agent.run(prompt, videos=[video_file])
        formatted_content = format_analysis(response.content)
        response_placeholder.markdown(formatted_content)

def main():
    st.set_page_config(page_title="Smart Video Analyzer", page_icon="🎥", layout="wide")
    load_custom_css()
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>✨ Smart Video Analyzer</h1>
            <p>Powered by Advanced AI | Precise Analysis | Web Research</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize agent
    agent = create_agent()
    
    # File upload
    st.subheader("📤 Upload Your Video")
    video_file = st.file_uploader(
        "",
        type=['mp4', 'mov', 'avi'],
        help="Supporting MP4, MOV, and AVI formats"
    )
    
    if video_file:
        video_path = process_video_file(video_file)
        st.video(video_path)
        
        st.subheader("🤔 What would you like to know?")
        query = st.text_area(
            "",
            placeholder="Ask anything about the video...",
            help="Be specific for better results",
            value="Please analyze this video and provide key observations, insights, and relevant context."
        )
        
        if st.button("🔍 Analyze Video", key="analyze_button"):
            if not query:
                st.error("⚠️ Please enter your question first!")
            else:
                try:
                    processed_file = upload_file(video_path)
                    while processed_file.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_file = get_file(processed_file.name)
                    
                    prompt = f"""
                    Analyze this video addressing: "{query}"
                    
                    Format your response using these sections:
                    **Content Focus**
                    [Provide main content analysis]
                    
                    **Visual Style**
                    [Describe visual elements]
                    
                    **Presenter**
                    [Describe presenter characteristics]
                    
                    **Step Breakdown**
                    [List key steps if applicable]
                    
                    **Key Points**
                    [Summarize main takeaways]
                    
                    Make it clear and concise.
                    """
                    
                    st.subheader("✨ Analysis Results")
                    response_placeholder = st.empty()
                    stream_analysis(response_placeholder, agent, prompt, processed_file)
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                finally:
                    Path(video_path).unlink(missing_ok=True)
    else:
        st.markdown("""
            ### 👋 Welcome to Smart Video Analyzer!
            Upload a video to get started with AI-powered analysis
        """)

def create_agent() -> Agent:
    """Initialize AI agent"""
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

# def load_custom_css():
#     """Load custom CSS for enhanced UI"""
#     st.markdown("""
#         <style>
#         /* Global styles */
#         .main {
#             background-color: #f5f7fa;
#         }
        
#         /* App container */
#         .stApp {
#             max-width: 1200px;
#             margin: 0 auto;
#         }
        
#         /* Header styling */
#         .app-header {
#             background: linear-gradient(120deg, #2E3192 0%, #1BFFFF 100%);
#             color: white;
#             padding: 2rem;
#             border-radius: 15px;
#             margin-bottom: 2rem;
#             text-align: center;
#         }
        
#         /* Analysis container */
#         .analysis-container {
#             background: white;
#             padding: 2rem;
#             border-radius: 15px;
#             box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#             margin-top: 2rem;
#         }
        
#         /* Section styling */
#         .section {
#             background: #f8f9fa;
#             padding: 1.5rem;
#             border-radius: 10px;
#             margin: 1rem 0;
#             border-left: 5px solid #4E65FF;
#         }
        
#         /* Text styling */
#         h1, h2, h3 {
#             color: #2E3192;
#             margin-bottom: 1rem;
#         }
        
#         p {
#             color: #333;
#             line-height: 1.6;
#         }
        
#         /* Custom elements */
#         .emoji-icon {
#             font-size: 1.2em;
#             margin-right: 0.5rem;
#         }
        
#         .highlight-text {
#             color: #4E65FF;
#             font-weight: bold;
#         }
#         </style>
#     """, unsafe_allow_html=True)

# def create_header():
#     """Create the app header"""
#     st.markdown(
#         """
#         <div class="app-header">
#             <h1>✨ Smart Video Analyzer</h1>
#             <p style="font-size: 1.2rem;">
#                 Powered by Advanced AI | Precise Analysis | Web Research
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# def format_analysis_section(title: str, content: str) -> str:
#     """Format an analysis section with consistent styling"""
#     return f"""
#     <div class="section">
#         <h3><span class="emoji-icon">{title.split()[0]}</span>{' '.join(title.split()[1:])}</h3>
#         <div class="content">
#             {content}
#         </div>
#     </div>
#     """

# def process_analysis_response(content: str) -> str:
#     """Process and format the analysis response"""
#     sections = {
#         "🎯 Key Observations": "",
#         "📊 Context & Insights": "",
#         "💡 Additional Research": ""
#     }
    
#     current_section = None
#     lines = content.split('\n')
    
#     for line in lines:
#         if any(section in line for section in sections.keys()):
#             current_section = next(key for key in sections.keys() if key in line)
#         elif current_section and line.strip():
#             sections[current_section] += f"<p>{line.strip()}</p>"
    
#     formatted_response = '<div class="analysis-container">'
#     for title, content in sections.items():
#         if content:
#             formatted_response += format_analysis_section(title, content)
#     formatted_response += '</div>'
    
#     return formatted_response

# def stream_analysis(response_placeholder, agent, prompt, video_file):
#     """Stream the analysis with loading state"""
#     with st.spinner("🤖 Analyzing your video..."):
#         response = agent.run(prompt, videos=[video_file])
#         formatted_response = process_analysis_response(response.content)
#         response_placeholder.markdown(formatted_response, unsafe_allow_html=True)

# def main():
#     st.set_page_config(
#         page_title="Smart Video Analyzer",
#         page_icon="🎥",
#         layout="wide"
#     )
    
#     load_custom_css()
#     create_header()
    
#     # Initialize AI agent
#     agent = create_agent()
    
#     # File upload section
#     st.markdown(
#         """
#         <div class="section">
#             <h2>📤 Upload Your Video</h2>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
    
#     video_file = st.file_uploader(
#         "",
#         type=['mp4', 'mov', 'avi'],
#         help="Support for MP4, MOV, and AVI formats"
#     )
    
#     if video_file:
#         video_path = process_video_file(video_file)
#         st.video(video_path)
        
#         st.markdown(
#             """
#             <div class="section">
#                 <h2>🤔 What would you like to know?</h2>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )
        
#         query = st.text_area(
#             "",
#             placeholder="Ask anything about the video...",
#             help="Be specific for better results",
#             value="Please provide a comprehensive analysis of this video including key points, insights, and relevant context."
#         )
        
#         if st.button("Analyze Video", key="analyze_button"):
#             if not query:
#                 st.error("⚠️ Please enter your question first!")
#             else:
#                 try:
#                     with st.spinner("Processing video..."):
#                         processed_file = upload_file(video_path)
#                         while processed_file.state.name == "PROCESSING":
#                             time.sleep(1)
#                             processed_file = get_file(processed_file.name)
                        
#                         prompt = f"""
#                         Analyze this video addressing: "{query}"
                        
#                         Structure your response with:
#                         🎯 Key Observations
#                         📊 Context & Insights
#                         💡 Additional Research
                        
#                         Make it clear and engaging.
#                         """
                        
#                         response_placeholder = st.empty()
#                         stream_analysis(response_placeholder, agent, prompt, processed_file)
                
#                 except Exception as e:
#                     st.error(f"Error: {str(e)}")
#                 finally:
#                     # Clean up temporary file
#                     Path(video_path).unlink(missing_ok=True)
#     else:
#         st.markdown(
#             """
#             <div class="section" style="text-align: center;">
#                 <h2>👋 Welcome!</h2>
#                 <p>Upload a video to start the AI analysis</p>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

# def create_agent() -> Agent:
#     """Initialize AI agent"""
#     return Agent(
#         name="Smart Video Analyzer",
#         model=Gemini(id="gemini-2.0-flash-exp"),
#         tools=[DuckDuckGo()],
#         markdown=True,
#     )

# def process_video_file(video_file) -> Optional[str]:
#     """Process uploaded video file"""
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
#         temp_file.write(video_file.read())
#         return temp_file.name

# if __name__ == "__main__":
#     main()