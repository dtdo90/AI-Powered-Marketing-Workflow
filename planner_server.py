from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from crewai import Crew, Task, Agent, LLM
from crewai_tools import SerperDevTool, WebsiteSearchTool
import nest_asyncio
from dotenv import load_dotenv
import os
import logging

nest_asyncio.apply()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize a server
server = Server()

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

MODEL = "gemini/gemini-2.0-flash"
llm = LLM(
    model=MODEL,
    api_key=gemini_api_key,
    temperature=0.7,  # Balanced for strategic planning
    max_tokens=4096   # Increased for comprehensive marketing plans
)

@server.agent()
async def marketing_planner(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    Marketing planner agent that automatically performs research, analysis, and creates comprehensive marketing plans.
    Uses CrewAI to orchestrate multiple specialized agents for a complete workflow.
    """    
    logger.info("Starting marketing planning process...")
    
    # Create specialized agents for different aspects of marketing planning
    market_researcher = Agent(
        role="Market Research Analyst",
        goal="Conduct comprehensive market research and competitive analysis to identify opportunities and trends",
        backstory=(
            "You are a senior market research analyst with 8+ years of experience in digital marketing research. "
            "You specialize in competitive analysis, trend identification, and market opportunity assessment. "
            "You have helped numerous companies understand their market position and identify growth opportunities. "
            "You excel at gathering and analyzing data from multiple sources to provide actionable insights."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[SerperDevTool(), WebsiteSearchTool()],
        max_retry_limit=3
    )
    
    strategy_consultant = Agent(
        role="Senior Marketing Strategy Consultant",
        goal="Develop comprehensive marketing strategies and tactical plans based on research insights",
        backstory=(
            "You are a senior marketing strategy consultant with 12+ years of experience in digital marketing. "
            "You have helped Fortune 500 companies and startups develop successful marketing strategies. "
            "You specialize in multi-channel marketing, customer journey optimization, and ROI-driven campaigns. "
            "You understand how to translate market insights into actionable marketing plans that drive results."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[SerperDevTool(), WebsiteSearchTool()],
        max_retry_limit=3
    )
    
    # Create tasks for the workflow
    research_task = Task(
        description=(
            f"Conduct comprehensive market research for: {input[0].parts[0].content}\n\n"
            "Research Requirements:\n"
            "1. Market size and growth trends\n"
            "2. Competitive landscape analysis\n"
            "3. Target audience demographics and behavior\n"
            "4. Industry best practices and emerging trends\n"
            "5. Potential challenges and opportunities\n"
            "6. Relevant case studies and success stories\n\n"
            "Provide detailed findings with data sources and actionable insights."
        ),
        expected_output=(
            "A comprehensive market research report including:\n"
            "- Market overview and size\n"
            "- Competitive analysis\n"
            "- Target audience insights\n"
            "- Industry trends and opportunities\n"
            "- Relevant case studies\n"
            "- Data sources and methodology"
        ),
        agent=market_researcher
    )
    
    strategy_task = Task(
        description=(
            "Based on the market research findings, develop a comprehensive marketing plan.\n\n"
            "Strategy Requirements:\n"
            "1. Executive Summary\n"
            "2. Market Analysis Summary\n"
            "3. Target Audience Analysis\n"
            "4. Marketing Strategy Overview\n"
            "5. Channel-Specific Tactics:\n"
            "   - Content Marketing\n"
            "   - Social Media Marketing\n"
            "   - SEO Strategy\n"
            "   - Paid Advertising\n"
            "   - Email Marketing\n"
            "   - Influencer Marketing\n"
            "6. Implementation Timeline (3-6 months)\n"
            "7. Budget Allocation Recommendations\n"
            "8. Success Metrics & KPIs\n"
            "9. Risk Assessment & Mitigation\n"
            "10. ROI Projections\n\n"
            "Format as a professional marketing plan document."
        ),
        expected_output=(
            "A complete marketing plan document with:\n"
            "- Executive summary\n"
            "- Detailed strategy sections\n"
            "- Implementation timeline\n"
            "- Budget breakdown\n"
            "- Success metrics\n"
            "- Risk assessment\n"
            "- Professional formatting and structure"
        ),
        agent=strategy_consultant
    )
    
    crew = Crew(
        agents=[market_researcher, strategy_consultant],
        tasks=[research_task, strategy_task],
        verbose=True
    )
    
    task_output = await crew.kickoff_async()

    yield Message(parts=[MessagePart(content=str(task_output))])
    

if __name__ == "__main__":
    server.run(port=8000)
