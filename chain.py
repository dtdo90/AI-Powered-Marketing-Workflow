from acp_sdk.client import Client
import asyncio 
from colorama import Fore, Style
import logging
from typing import Optional
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    context = {**config.DEFAULT_CONTEXT, **(company_context or {})}
    
    # Create structured input for the planner
    planner_input = create_planner_input(context, specific_request)

    async with Client(base_url=config.PLANNER_SERVER_URL) as planner, \
                Client(base_url=config.WRITER_SERVER_URL) as writer:
        
        logger.info("===== Starting marketing planning phase =====")
        
        # Step 1: Generate marketing plan
        run1 = await planner.run_sync(
            agent="marketing_planner", 
            input=planner_input
        )
        
        if not run1.output or not run1.output[0].parts:
            raise ValueError("No output received from marketing planner")
            
        marketing_plan = run1.output[0].parts[0].content
        print(f"{Fore.LIGHTMAGENTA_EX}📋 MARKETING PLAN:{Style.RESET_ALL}")
        print(f"{Fore.LIGHTMAGENTA_EX}{marketing_plan}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

        # Step 2: Generate blog content
        logger.info("======= Starting content creation phase ======")
        writer_input = create_writer_input(marketing_plan, context)
        
        run2 = await writer.run_sync(
            agent="supervisor_agent", 
            input=writer_input
        )
        
        if not run2.output or not run2.output[0].parts:
            raise ValueError("No output received from blog writer")
            
        blog_content = run2.output[0].parts[0].content
        print(f"{Fore.YELLOW}📝 BLOG CONTENT:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{blog_content}{Style.RESET_ALL}")
        
        # Save outputs to files
        
        # Create output directory if it doesn't exist
        output_dir = "marketing_outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save marketing plan
        plan_filename = f"{output_dir}/marketing_plan.md"
        with open(plan_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Marketing Plan\n\n")
            f.write(f"**Company:** {context['company_type']}\n")
            f.write(f"**Industry:** {context['industry']}\n\n")
            f.write(marketing_plan)
        
        # Save blog content
        blog_filename = f"{output_dir}/blog_post.md"
        with open(blog_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Blog Post\n\n")
            f.write(f"**Company:** {context['company_type']}\n")
            f.write(f"**Industry:** {context['industry']}\n\n")
            f.write(blog_content)
        
        
        return {
            "marketing_plan": marketing_plan,
            "blog_content": blog_content,
            "context": context,
            "status": "success",
            "files": {
                "marketing_plan": plan_filename,
                "blog_post": blog_filename
            }
        }
        

def create_planner_input(context: dict, specific_request: Optional[str] = None) -> str:
    """Create a structured input for the marketing planner"""
    base_prompt = f"""
Create a comprehensive marketing strategy for {context['company_type']} in the {context['industry']} industry.

COMPANY CONTEXT:
- Company Type: {context['company_type']}
- Industry: {context['industry']}
- Target Audience: {context['target_audience']}
- Value Proposition: {context['value_proposition']}
- Key Benefits: {', '.join(context['key_benefits'])}

SPECIFIC REQUEST: {specific_request or 'Create a comprehensive marketing strategy to increase brand awareness and drive customer acquisition'}

REQUIREMENTS:
1. Research current marketing trends in the AI/tech industry
2. Identify target audience segments and their pain points
3. Develop a multi-channel marketing strategy
4. Include specific tactics for:
   - Content marketing
   - Social media
   - SEO optimization
   - Lead generation
   - Customer acquisition
5. Provide measurable KPIs and success metrics
6. Include budget allocation recommendations
7. Timeline for implementation

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

def create_writer_input(marketing_plan: str, context: dict) -> str:
    """Create a structured input for the blog writer"""
    return f"""
Write a compelling, SEO-optimized blog post based on the following marketing strategy.

MARKETING STRATEGY:
{marketing_plan}

COMPANY CONTEXT:
- Company: {context['company_type']}
- Industry: {context['industry']}
- Target Audience: {context['target_audience']}

BLOG POST REQUIREMENTS:
1. Create an engaging headline that includes relevant keywords
2. Write a compelling introduction that hooks the reader
3. Structure the content with clear headings and subheadings
4. Include actionable insights and practical tips
5. Optimize for SEO with relevant keywords naturally integrated
6. Include a strong call-to-action
7. Target length: 1000-1500 words
8. Tone: Professional yet approachable
9. Include relevant statistics and examples where appropriate

IMPORTANT: Write the blog post in clean markdown format, ready-to-publish. Do NOT include labels like "SEO-Optimized Headline:" or "Meta Description:". 
Just write the actual blog post content with proper markdown formatting (headings, paragraphs, lists, etc.).
Start directly with the main headline and content.
"""

if __name__ == "__main__":
    # Example usage with custom context
    comany_context = {
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
    
    asyncio.run(run_marketing_workflow(
        company_context=comany_context,
        specific_request="Create a marketing strategy to launch our new AI-powered marketing automation platform"
    ))