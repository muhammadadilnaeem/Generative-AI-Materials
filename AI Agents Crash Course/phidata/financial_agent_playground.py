
# Import necessary libraries
import phi
import phi.api
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.playground import Playground, serve_playground_app
from dotenv import load_dotenv
import os  # Import os to access environment variables

# Load environment variables from a .env file
load_dotenv()

# Set the GROQ_API_KEY from the environment variable
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment variables.")

# Set the PHIDATA_API_KEY from the environment variable
PHIDATA_API_KEY = os.getenv('PHIDATA_API_KEY')
if not PHIDATA_API_KEY:
    raise ValueError("PHIDATA_API_KEY not set in environment variables.")  # Fixed error message

# Create agents

# 1. Create a web search agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search web for the required information",
    model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_API_KEY),  # Pass the GROQ API key to the model
    tools=[DuckDuckGo()],
    instructions=['Always include sources of information'],  # Instructions for the agent
    show_tool_calls=True,  # Show tool calls in the output
    markdown=True,  # Use Markdown for formatting
)

# 2. Create a financial stock agent
finance_agent = Agent(
    name="Finance Agent",
    model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_API_KEY),  # Pass the GROQ API key to the model
    tools=[
        YFinanceTools(
            stock_price=True, 
            analyst_recommendations=True,
            stock_fundamentals=True, 
            company_info=True, 
            company_news=True
        )
    ],
    instructions=['Hey, Use Tables to Display the Data beautifully.'],  # Instructions for the agent
    show_tool_calls=True,  # Show tool calls in the output
    markdown=True,  # Use Markdown for formatting
)

# Create a Playground app with the defined agents
app = Playground(agents=[finance_agent, web_search_agent]).get_app()

# Main entry point for the application
if __name__ == "__main__":
    # Serve the Playground app
    serve_playground_app("financial_agent_playground:app", reload=True)