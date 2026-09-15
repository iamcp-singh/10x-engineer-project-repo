# PromptLab

**Your AI Prompt Engineering Platform**

---

## Welcome to the Team! 👋

Congratulations on joining the PromptLab engineering team! You've been brought on to help us build the next generation of prompt engineering tools.

### What is PromptLab?

PromptLab is an internal tool for AI engineers to **store, organize, and manage their prompts**. Think of it as a "Postman for Prompts" — a professional workspace where teams can:

- 📝 Store prompt templates with variables (`{{input}}`, `{{context}}`)
- 📁 Organize prompts into collections
- 🏷️ Tag and search prompts
- 📜 Track version history
- 🧪 Test prompts with sample inputs

### The Current Situation

The backend is functional. Four known bugs have been fixed and `PATCH` support has been added. The core structure is in place:

- Some **features are incomplete**
- The **documentation is minimal** (you'll improve that)
- **Tests are present** and cover basic functionality
- **No CI/CD pipeline** exists yet
- **No frontend** has been built yet

Your job over the next 4 weeks is to transform this into a **production-ready, full-stack application**.

---

### Quick Start

### Prerequisites

- Python 3.10+
- Git

### Run Locally

```bash
# Clone the repo
git clone https://github.com/iamcp-singh/10x-engineer-project-repo.git
cd 10x-engineer-project-repo

# Create and activate a Python virtual environment (macOS / Linux)
python -m venv .venv
source .venv/bin/activate

cd backend
pip install -r requirements.txt
pytest tests/ -v
python main.py
```

API runs at: http://localhost:8000

API docs at: http://localhost:8000/docs

### Run Tests

```bash
# From the repository root or inside `backend` with the venv activated
cd backend
pytest tests/ -v
```

---

## Project Structure

```
10x-engineer-project-repo/
├── README.md                    # You are here
├── PROJECT_BRIEF.md             # Your assignment details
├── GRADING_RUBRIC.md            # How you'll be graded
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api.py              # FastAPI routes
│   │   ├── models.py           # Pydantic models
│   │   ├── storage.py          # In-memory storage
│   │   └── utils.py            # Helper functions
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py         # API tests
│   │   └── conftest.py         # Test fixtures
│   ├── main.py                 # Entry point
│   └── requirements.txt
│
├── frontend/                    # You'll create this in Week 4
├── specs/                       # You'll create this in Week 2
├── docs/                        # You'll create this in Week 2
└── .github/                     # You'll set up CI/CD in Week 3
```

---

## Your Mission

### 🧪 Experimentation Encouraged!
While we provide guidelines, **you are the engineer**. If you see a better way to solve a problem using AI, do it!
- Want to swap the storage layer for a real database? **Go for it.**
- Want to add Authentication? **Do it.**
- Want to rewrite the API in a different style? **As long as tests pass, you're clear.**

The goal is to learn how to build *better* software *faster* with AI. Don't be afraid to break things and rebuild them better.

### Week 1: Fix the Backend
- Understand this codebase using AI
- Find and fix the bugs
- Implement missing features

### Week 2: Document Everything
- Write proper documentation
- Create feature specifications
- Set up coding standards

### Week 3: Make it Production-Ready
- Write comprehensive tests
- Implement new features with TDD
- Set up CI/CD and Docker

### Week 4: Build the Frontend
- Create a React frontend
- Connect it to the backend
- Polish the user experience

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/prompts` | List all prompts |
| GET | `/prompts/{id}` | Get single prompt |
| POST | `/prompts` | Create prompt |
| PUT | `/prompts/{id}` | Update prompt |
| PATCH | `/prompts/{id}` | Partially update prompt |
| DELETE | `/prompts/{id}` | Delete prompt |
| GET | `/collections` | List collections |
| GET | `/collections/{id}` | Get collection |
| POST | `/collections` | Create collection |
| DELETE | `/collections/{id}` | Delete collection |

---

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic
- **Frontend**: React, Vite (Week 4)
- **Testing**: pytest
- **DevOps**: Docker, GitHub Actions (Week 3)

---

Good luck, and welcome to the team! 🚀
