# AI-Powered Marketing Workflow

An intelligent marketing automation system that uses the Agent Communication Protocol (ACP) to create comprehensive marketing strategies and generate SEO-optimized content. This project combines multiple AI agents to deliver end-to-end marketing solutions.

## 🚀 Features

- **Intelligent Marketing Planning**: Automated market research and strategy development
- **SEO-Optimized Content Creation**: Generate engaging blog posts with built-in SEO optimization
- **Multi-Agent Architecture**: Uses CrewAI with specialized agents for different marketing tasks
- **Real-time Research**: Integrates with search tools for up-to-date market insights
- **Output Management**: Automatically saves marketing plans and blog content to files

## 🏗️ Architecture

The system consists of three main components:

1. **Planner Server** (`planner_server.py`): Handles market research and strategy development
2. **Writer Server** (`writer_server.py`): Creates SEO-optimized blog content
3. **Main Chain** (`chain.py`): Orchestrates the complete workflow

### Agent Roles

- **Market Research Analyst**: Conducts comprehensive market research and competitive analysis
- **Marketing Strategy Consultant**: Develops strategic marketing plans
- **Content Marketing Specialist**: Creates engaging, SEO-optimized blog posts
- **Content Editor**: Cleans and formats content for publication

## 📋 Prerequisites

- Python 3.10+
- Gemini API key (Google AI)
- Internet connection for research tools

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd acp_marketing
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

## 🚀 Quick Start

1. **Start the servers** (in separate terminals):
   ```bash
   # Terminal 1 - Start planner server
   python planner_server.py
   
   # Terminal 2 - Start writer server
   python writer_server.py
   ```

2. **Run the marketing workflow**:
   ```bash
   python chain.py
   ```

## 📖 Usage

### Basic Usage

The system will use default settings for an AI startup. Simply run:

```bash
python chain.py
```

### Custom Company Context

You can customize the company context by modifying the `company_context` in `chain.py`:

```python
company_context = {
    "company_type": "Your Company Type",
    "industry": "Your Industry",
    "target_audience": "Your Target Audience",
    "value_proposition": "Your Value Proposition",
    "key_benefits": ["Benefit 1", "Benefit 2", "Benefit 3"]
}
```

### Specific Marketing Requests

You can also provide specific marketing requests:

```python
specific_request = "Create a social media marketing strategy for Q4"
```

## 📁 Output Structure

The system generates two main outputs in the `marketing_outputs/` directory:

- `marketing_plan.md`: Comprehensive marketing strategy document
- `blog_post.md`: SEO-optimized blog content

### Marketing Plan Includes:
- Executive Summary
- Market Analysis
- Target Audience Analysis
- Marketing Strategy Overview
- Channel-Specific Tactics
- Implementation Timeline
- Budget Allocation
- Success Metrics & KPIs
- Risk Assessment

### Blog Post Features:
- SEO-optimized headlines
- Engaging introductions
- Well-structured content
- Actionable insights
- Strong calls-to-action
- Natural keyword integration

## 🔧 API Endpoints

### Planner Server (Port 8000)
- `marketing_planner`: Generates comprehensive marketing strategies

### Writer Server (Port 8001)
- `blog_writer`: Creates SEO-optimized blog content
- `supervisor_agent`: Cleans and formats content for publication

## 🛠️ Project Structure
```
acp_marketing/
├── chain.py              # Main workflow orchestration
├── planner_server.py     # Marketing planning server
├── writer_server.py      # Content creation server
├── requirements.txt     # Python dependencies
├── marketing_outputs/   # Generated content
│   ├── marketing_plan.md
│   └── blog_post.md
└── README.md
```

