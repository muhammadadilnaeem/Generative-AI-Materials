

# Import necessary libraries
import phi 
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os  # Import os to access environment variables

# Load environment variables from a .env file
load_dotenv()

# Set the GROQ_API_KEY from the environment variable
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment variables.")

# Create agents

# 1. Create a web search agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search web for the required information",
    model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_API_KEY),  # Pass the API key to the model
    tools=[DuckDuckGo()],
    instructions=['Always include sources of information'],
    show_tool_calls=True,
    markdown=True,
)

# 2. Create a financial stock agent
finance_agent = Agent(
    name="Finance Agent",
    model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_API_KEY),  # Pass the API key to the model
    tools=[
        YFinanceTools(stock_price=True, 
                      analyst_recommendations=True,
                      stock_fundamentals=True, 
                      company_info=True, 
                      company_news=True)
    ],
    instructions=['Hey, Use Tables to Display the Data beautifully.'],
    show_tool_calls=True,
    markdown=True,               
)

# Combine both agents to make a new agent
mr_finance_agent = Agent(
    team=[web_search_agent, finance_agent],
    instructions=['Hey, Always include sources of information. Use Tables to Display the Data effectively.'],
    show_tool_calls=True,
    markdown=True,
)

# Initiate 'mr_finance_agent' and print the response
mr_finance_agent.print_response("Summarize Analyst Recommendation and Share the Latest News for NVDA", stream=True)