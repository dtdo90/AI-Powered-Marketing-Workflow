# Multi-Agent Marketing Workflow

> **AI-powered marketing automation that thinks, plans, and creates like a full marketing team**

An intelligent marketing system using **Agent Communication Protocol (ACP)** to orchestrate specialized AI agents that deliver comprehensive marketing strategies and SEO-optimized content automatically.

## ✨ Key Features

🤖 **Multi-Agent Orchestration** - ACP-powered distributed agents work together seamlessly  
📊 **Intelligent Strategy Planning** - Data-driven market research and competitive analysis  
🔄 **Automated Workflows** - End-to-end marketing pipeline without manual intervention  

✍️ **SEO-Optimized Content** - Professional blog posts and marketing materials  

## 🏗️ Architecture

**3-Layer System:**
- **🧠 Planner Server** (Port 8000): Market research & strategy development
- **✍️ Writer Server** (Port 8001): SEO-optimized content creation  
- **🎯 Orchestrator**: Intelligent task delegation and workflow management

**Specialized AI Agents:**
- Market Research Analyst
- Marketing Strategy Consultant  
- Content Marketing Specialist
- Content Editor

## ⚡ Quick Start

1. **Setup**:
   ```bash
   git clone <repository-url> && cd acp_marketing
   uv sync
   ```

2. **Configure API keys** in `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   SERPER_API_KEY=your_serper_api_key  
   OPENAI_API_KEY=your_openai_api_key # put a dummy key for SerperDevTool
   ```

3. **Launch** (3 terminals):
   ```bash
   # Terminal 1: Planner
   uv run planner_server.py
   
   # Terminal 2: Writer  
   uv run writer_server.py
   
   # Terminal 3: Execute workflow
   uv run chain.py
   ```

## 🎯 Usage

**Default AI Startup Template:**
```bash
uv run chain.py
```

**Custom Company Context:**
```python
company_context = {
    "company_type": "SaaS Platform",
    "industry": "FinTech", 
    "target_audience": "Financial professionals",
    "value_proposition": "Automated financial reporting",
    "key_benefits": ["Real-time analytics", "Compliance automation"]
}
```

## 📊 Output

**Generated in `marketing_outputs/`:**


📝 **`blog_post.md`** - Publication-ready content
- SEO-optimized headlines & structure
- Engaging copy with CTAs
- Strategic keyword integration

## 🔧 API Endpoints

| Server | Port | Endpoint | Function |
|--------|------|----------|----------|
| Planner | 8000 | `marketing_planner` | Strategy generation |
| Writer | 8001 | `blog_writer` | Content creation |
| Writer | 8001 | `supervisor_agent` | Content optimization |

## 📁 Project Structure
```
acp_marketing/
├── 🎯 chain.py              # Main orchestrator
├── 🧠 planner_server.py     # Strategy server  
├── ✍️ writer_server.py      # Content server
├── 📦 requirements.txt      # Dependencies
├── 📊 marketing_outputs/    # Generated content
└── 📖 README.md
```

---
*Transform your marketing workflow with AI agents that work 24/7* 🌟

