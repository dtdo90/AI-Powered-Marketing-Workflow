from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from crewai import Crew, Task, Agent, LLM
from crewai_tools import SerperDevTool, WebsiteSearchTool
import nest_asyncio
from dotenv import load_dotenv
import os
import logging
import re

nest_asyncio.apply()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize a server
server = Server()

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    logger.warning("GEMINI_API_KEY not found in environment variables. Using empty string.")

MODEL = "gemini/gemini-2.0-flash"
llm = LLM(
    model=MODEL,
    api_key=gemini_api_key,
    temperature=0.8,  # Slightly higher for more creative content
    max_tokens=8192   # Increased for longer blog posts
)

# Define agent on the server
@server.agent()
async def blog_writer(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    Expert content writer agent that creates SEO-optimized, engaging blog posts.
    Specializes in tech and marketing content with strong conversion optimization.
    """
 
    logger.info("Starting blog content creation process...")
    
    content_writer = Agent(
        role="Senior Content Marketing Specialist",
        goal="Create high-converting, SEO-optimized blog posts that drive engagement and conversions",
        backstory=(
            "You are a senior content marketing specialist with 10+ years of experience in digital marketing "
            "and content creation. You have a proven track record of creating viral blog posts that generate "
            "millions of views and thousands of leads. You specialize in tech and marketing content, with deep "
            "expertise in SEO, conversion optimization, and audience engagement. You understand how to write "
            "content that ranks well in search engines while maintaining high readability and engagement rates. "
            "You have helped numerous startups and tech companies build their content marketing strategies "
            "and achieve significant growth through content-driven lead generation."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[SerperDevTool(), WebsiteSearchTool()],
        max_retry_limit=3
    )

    # Create a task for content creation
    task = Task(
        description=input[0].parts[0].content,
        expected_output=(
            "Write a complete, SEO-optimized blog post (1000-1500 words) with:\n"
            "- Engaging headline and meta description\n"
            "- Compelling introduction\n"
            "- Well-structured content with clear headings\n"
            "- Actionable insights and examples\n"
            "- Strong conclusion with call-to-action\n"
            "- Natural keyword integration\n"
            "- SEO considerations and internal linking suggestions\n"
            "- Meta tags and schema markup recommendations\n\n"
            "Include all the technical SEO elements and meta-information that would be useful for publishing."
        ),
        agent=content_writer
    )
    
    logger.info("Creating crew and executing task...")
    crew = Crew(
        agents=[content_writer], 
        tasks=[task], 
        verbose=True
    )
    
    task_output = await crew.kickoff_async()
    yield Message(parts=[MessagePart(content=str(task_output))])

@server.agent()
async def supervisor_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    Supervisor agent that takes blog content and converts it to ready-to-use format.
    Removes meta-instructions, SEO considerations, and formatting guidelines.
    """
    
    logger.info("Starting content supervision and cleanup process...")
    
    supervisor = Agent(
        role="Content Editor and Publisher",
        goal="Transform raw blog content into clean, ready-to-publish format",
        backstory=(
            "You are an experienced content editor and publisher with expertise in preparing content "
            "for publication. You understand the difference between raw content with instructions and "
            "clean, publishable content. You excel at removing meta-information, formatting guidelines, "
            "and technical instructions while preserving the core message and value of the content. "
            "You ensure content is properly formatted for immediate use in content management systems, "
            "blogs, and other publishing platforms."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[],
        max_retry_limit=3
    )

    # Create a task for content cleanup
    task = Task(
        description=(
            f"Take the following blog content and convert it to a clean, ready-to-publish format:\n\n"
            f"{input[0].parts[0].content}\n\n"
            f"Your task is to:\n"
            f"1. Remove all meta-instructions and formatting guidelines\n"
            f"2. Remove 'SEO Considerations' sections\n"
            f"3. Remove 'Internal Linking Suggestions' sections\n"
            f"4. Remove 'Meta Tags and Schema Markup Suggestions' sections\n"
            f"5. Remove keyword lists and technical SEO instructions\n"
            f"6. Keep only the actual blog post content\n"
            f"7. Ensure proper markdown formatting\n"
            f"8. Start with the main headline\n"
            f"9. End with a strong conclusion and call-to-action\n"
            f"10. Make sure the content flows naturally without any meta-information\n\n"
            f"Output ONLY the clean, ready-to-publish blog post content."
        ),
        expected_output=(
            "A clean, ready-to-publish blog post in markdown format that includes:\n"
            "- Main headline\n"
            "- Introduction\n"
            "- Well-structured content with headings\n"
            "- Conclusion with call-to-action\n"
            "- No meta-instructions or technical guidelines\n"
            "- No SEO considerations or keyword lists\n"
            "- No formatting instructions\n"
            "- Content that can be directly copied and pasted into a CMS"
        ),
        agent=supervisor
    )
    
    logger.info("Creating supervisor crew and executing cleanup task...")
    crew = Crew(
        agents=[supervisor], 
        tasks=[task], 
        verbose=True
    )
    
    task_output = await crew.kickoff_async()
    yield Message(parts=[MessagePart(content=str(task_output))])

if __name__ == "__main__":
    server.run(port=8001) 