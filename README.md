# 🏗️ AI Website Builder

A multi-agent system that generates complete, functional websites from natural language descriptions. Built with **CrewAI**, this project simulates a development team where specialized AI agents collaborate to plan, build, and test websites autonomously.


## 🎯 What It Does

Describe the website you want in plain English, and the AI crew handles everything:

```
You: "Build me a portfolio website with a dark theme, 
     an about section, project gallery, and contact form"

AI Crew: Plans → Codes Frontend → Codes Backend → Integrates → Tests
         ↓
         Ready-to-run website in /website folder
```

The system also supports **editing existing websites** - just describe what you want to change.

## 🤖 The AI Team

This project implements a virtual development team where each agent has a specialized role:

| Agent | Role | Responsibilities |
|-------|------|------------------|
| **Team Lead** | Project Planner | Analyzes requirements, defines tech stack, creates file structure |
| **Frontend Dev** | UI Developer | Writes HTML, CSS, JavaScript with responsive design |
| **Backend Dev** | Server Developer | Implements Flask routes, form handlers, API endpoints |
| **Integrator** | DevOps Engineer | Creates directories, writes files to disk, assembles project |
| **Tester** | QA Engineer | Validates file structure, checks code quality, provides run instructions |

For editing existing sites, an **Analyzer** agent first reviews the current codebase before modifications.

## 🏛️ Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        User Input                               │
│              "Build me a portfolio website..."                  │
└───────────────────────────┬────────────────────────────────────┘
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                     Intent Router (LLM)                        │
│                    NEW website? or EDIT?                       │
└───────────┬───────────────────────────────────────┬───────────┘
            ▼                                       ▼
┌───────────────────────┐           ┌───────────────────────┐
│   SiteBuilderCrew     │           │     EditorCrew        │
│                       │           │                       │
│  ┌─────────────────┐  │           │  ┌─────────────────┐  │
│  │   Team Lead     │  │           │  │    Analyzer     │  │
│  │  (plan.json)    │  │           │  │ (reads codebase)│  │
│  └────────┬────────┘  │           │  └────────┬────────┘  │
│           ▼           │           │           ▼           │
│  ┌─────────────────┐  │           │  ┌─────────────────┐  │
│  │  Frontend Dev   │  │           │  │     Editor      │  │
│  │ (HTML/CSS/JS)   │  │           │  │ (modifications) │  │
│  └────────┬────────┘  │           │  └────────┬────────┘  │
│           ▼           │           │           ▼           │
│  ┌─────────────────┐  │           │  ┌─────────────────┐  │
│  │  Backend Dev    │  │           │  │   Integrator    │  │
│  │ (Flask/Python)  │  │           │  │ (writes files)  │  │
│  └────────┬────────┘  │           │  └────────┬────────┘  │
│           ▼           │           │           ▼           │
│  ┌─────────────────┐  │           │  ┌─────────────────┐  │
│  │   Integrator    │  │           │  │     Tester      │  │
│  └────────┬────────┘  │           │  └─────────────────┘  │
│           ▼           │           │                       │
│  ┌─────────────────┐  │           └───────────────────────┘
│  │     Tester      │  │
│  └─────────────────┘  │
└───────────────────────┘
            ▼
┌───────────────────────────────────────────────────────────────┐
│                      /website folder                           │
│         Complete, tested, ready-to-run website                 │
└───────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [DeepSeek API key](https://platform.deepseek.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/AhmedHAlshaer/AI-Website-Builder.git
cd AI-Website-Builder

# Install dependencies
pip install crewai crewai-tools python-dotenv

# Set up environment
cp .env.example .env
# Add your DEEPSEEK_API_KEY to .env
```

### Usage

```bash
python -m builder.main
```

You'll be prompted to choose between creating a new website or editing an existing one:

```
🌐 Welcome to the AI Website Builder!
============================================================

Hi! How can I help you today?
Do you want to work on a (N)ew website or (E)dit an existing one?
```

### Example Prompts

**Creating a new website:**
```
Build a restaurant website with:
- Homepage with hero image and daily specials
- Menu page organized by category
- Reservation form with date/time picker
- Contact page with embedded map
- Dark elegant theme with gold accents
```

**Editing an existing website:**
```
Add a testimonials section to the homepage with a carousel 
showing customer reviews. Also add a newsletter signup form 
in the footer.
```

## 📁 Project Structure

```
AI-Website-Builder/
├── builder/
│   ├── __init__.py
│   ├── main.py              # Entry point & intent routing
│   ├── crew.py              # SiteBuilderCrew definition
│   ├── editor_crew.py       # EditorCrew for modifications
│   ├── tools.py             # Custom filesystem tools
│   └── config/
│       ├── agents.yaml      # Agent roles & configurations
│       ├── tasks.yaml       # Task definitions (new sites)
│       └── editor_tasks.yaml # Task definitions (editing)
├── website/                 # Generated website output
├── .env.example
├── pyproject.toml
└── README.md
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Agent Framework** | CrewAI |
| **LLM Backend** | DeepSeek |
| **Generated Sites** | HTML, CSS, JavaScript, Flask (Python) |
| **Configuration** | YAML-based agent/task definitions |

## ✨ Key Features

- **Natural Language Input** - Describe your website in plain English
- **Multi-Agent Collaboration** - Specialized agents work together like a real dev team
- **Two Modes** - Create new websites or edit existing ones
- **Full-Stack Generation** - Frontend + backend when needed
- **Built-in QA** - Tester agent validates output before delivery
- **Custom Tools** - File system operations for real code generation

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | ✅ | API key from DeepSeek |
| `DEEPSEEK_MODEL` | Optional | Model name (default: `deepseek-chat`) |

## 🎓 Learning Outcomes

This project demonstrates:
- Building **multi-agent AI systems** with CrewAI
- Implementing **role-based agent architectures** (simulating a dev team)
- Creating **custom tools** for AI agents
- Using **YAML configuration** for agent/task definitions
- **Sequential task orchestration** with context passing between agents
- Practical **code generation** that produces runnable applications

## 📄 License

MIT License - feel free to use and modify.

## 👤 Author

**Ahmed H. Alshaer**  
Computer Science @ Indiana University Bloomington  
[GitHub](https://github.com/AhmedHAlshaer)
