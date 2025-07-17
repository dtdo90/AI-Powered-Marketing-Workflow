import asyncio
import nest_asyncio
from acp_sdk.client import Client
from acp_marketing.fastacp import AgentCollection, ACPCallingAgent, ChatMessage, ToolCall
from colorama import Fore
from typing import Optional
from crewai import LLM

from dotenv import load_dotenv
import os
import json

nest_asyncio.apply()

load_dotenv()
model = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    max_tokens=2048
)

class MarketingWorkflowConfig:
    """Configuration for the marketing workflow"""
    PLANNER_SERVER_URL = "http://localhost:8000"
    WRITER_SERVER_URL = "http://localhost:8001"
    
    # Default marketing context
    DEFAULT_CONTEXT = {
        "company_type": "AI startup",
        "industry": "Marketing Technology",
        "target_audience": "Marketing professionals, business owners, and growth teams",
        "value_proposition": "AI-powered marketing optimization and content creation",
        "key_benefits": [
            "Automated content generation",
            "SEO optimization",
            "Audience targeting",
            "Performance analytics"
        ]
    }

async def run_marketing_workflow(
    company_context: Optional[dict] = None,
    specific_request: Optional[str] = None
) -> dict:
    """
    Run the complete marketing workflow from planning to content creation.
    
    Args:
        company_context: Optional company-specific context
        specific_request: Optional specific marketing request
    
    Returns:
        dict: Complete workflow results
    """    
    config = MarketingWorkflowConfig()
    # start with default-context dictionary, overriding with company_context if provided
    context = {**config.DEFAULT_CONTEXT, **(company_context or {})}
    async with Client(base_url="http://localhost:8000") as planner, Client(base_url="http://localhost:8001") as writer:
        # agents discovery
        agent_collection=await AgentCollection.from_acp(planner, writer)
        print(f"Discovered agents: {[agent.name for client, agent in agent_collection.agents]}")

        # dictionary structure for ACPCallingAgent
        acp_agents={agent.name: {'agent': agent, 'client': client} for client, agent in agent_collection.agents}
        # passing the agents as tools to ACPCallingAgent with CrewAI LLM
        acpagent=ACPCallingAgent(
            acp_agents=acp_agents,
            model=model
        )
        
        # Create structured input for the planner
        formatted_input = format_input_for_acp_orchestrator(context, specific_request)

        # running the agent with a user query
        result = await acpagent.run(formatted_input)
        print(Fore.YELLOW + f"Final result:\n{result}" + Fore.RESET)

        # Save blog content
        output_dir = "marketing_outputs"
        os.makedirs(output_dir, exist_ok=True)

        blog_filename = f"{output_dir}/blog_post.md"
        with open(blog_filename, 'w', encoding='utf-8') as f:
            f.write(f"**Company:** {context['company_type']}\n")
            f.write(f"**Industry:** {context['industry']}\n\n")
            f.write(result)



def format_input_for_acp_orchestrator(context: dict, specific_request: Optional[str] = None) -> str:
    """
    Create a user prompt for the ACPCallingAgent, focusing on the business/content request and context.
    """
    base_prompt = f"""
Create a marketing blog post for {context['company_type']} in the {context['industry']} industry.

COMPANY CONTEXT:
- Company Type: {context['company_type']}
- Industry: {context['industry']}
- Target Audience: {context['target_audience']}
- Value Proposition: {context['value_proposition']}
- Key Benefits: {', '.join(context['key_benefits'])}

SPECIFIC REQUEST: {specific_request or 'Create a comprehensive marketing strategy to increase brand awareness and drive customer acquisition.'}

REQUIREMENTS:
- Research current marketing trends in the AI/tech industry.
- Identify target audience segments and their pain points.
- Develop a multi-channel marketing strategy.
- Include specific tactics for:
   - Content marketing
   - Social media
   - SEO optimization
   - Lead generation
   - Customer acquisition

OUTPUT FORMAT:
- Executive Summary
- Market Analysis
- Target Audience Analysis
- Marketing Strategy Overview
- Channel-Specific Tactics
- Implementation Timeline
- Budget Allocation
- Success Metrics & KPIs
- Risk Assessment
"""
    return base_prompt.strip()


if __name__ == "__main__":
    # Example usage with custom context
    company_context = {
        "company_type": "AI-powered marketing automation platform",
        "industry": "SaaS Marketing Technology",
        "target_audience": "Marketing managers, CMOs, and growth hackers",
        "value_proposition": "Automate your entire marketing funnel with AI",
        "key_benefits": [
            "10x faster content creation",
            "Automated A/B testing",
            "Predictive analytics",
            "Multi-channel campaign management"
        ]
    }
    
    print("Starting ACP Marketing Workflow...")
    
    asyncio.run(run_marketing_workflow(
        company_context=company_context,
        specific_request="Create a marketing strategy to launch our new AI-powered marketing automation platform"
    )) 