# PromptLab

**Your AI Prompt Engineering Platform**

---

## Welcome to the Team! 👋

Congratulations on joining the PromptLab engineering team! You've been brought on to help us build the next generation of prompt engineering tools.

## Project Overview

PromptLab is a lightweight backend service for managing AI prompts and collections.
It provides a simple HTTP API for creating, reading, updating, and deleting prompts,
optionally grouping them into collections.

PromptLab is intended for AI engineers, prompt engineers, and data scientists who
need a repeatable way to store and organize prompt templates while they iterate on
models and experiments. In its current state, PromptLab focuses on:

- A clear, test-backed FastAPI backend for prompt and collection management
- Serving as a foundation for future features such as tagging, version history,
  and prompt testing

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

## Features

### Currently Available

- **Prompt management API**
  - Create, read, update (`PUT`), partially update (`PATCH`), and delete prompts
  - Each prompt has a title, content, optional description, and optional
    `collection_id`
  - Server-side validation using Pydantic models
- **Collection management API**
  - Create, list, retrieve, and delete collections
  - When a collection is deleted, any prompts assigned to it are retained and
    their `collection_id` is set to `null`
- **Listing and search helpers**
  - List all prompts and collections
  - Filter prompts by `collection_id`
  - Search prompts by title and description text
  - Prompts are returned sorted by creation time (newest first)
- **Health check endpoint**
  - Simple `/health` endpoint exposing service status and version

### Planned / Future (Not Yet Implemented)

These capabilities are part of the broader vision but are **not yet fully
implemented** in the current codebase:

- Tagging prompts with arbitrary labels
- Tracking multiple versions / history of a prompt
- Interactive prompt testing workflows and UI
- Persistent storage (database) instead of in-memory storage

---

## Prerequisites and Installation

### Prerequisites

- Python 3.10+
- Git
- A POSIX-compatible shell (macOS / Linux) or PowerShell / Command Prompt (Windows)

### Installation

```bash
# Clone the repo
git clone https://github.com/iamcp-singh/10x-engineer-project-repo.git
cd 10x-engineer-project-repo

# Create a Python virtual environment
python -m venv .venv

# Activate the virtual environment
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell or cmd)
.venv\\Scripts\\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

To verify your installation, run the test suite:

```bash
pytest tests/ -v
```

---

## Quick Start

This is the shortest path from clone to a running API.

```bash
# 1. Clone the repo
git clone https://github.com/iamcp-singh/10x-engineer-project-repo.git
cd 10x-engineer-project-repo

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # on Windows use: .venv\\Scripts\\activate

# 3. Install backend dependencies
cd backend
pip install -r requirements.txt

# 4. Run tests (optional but recommended)
pytest tests/ -v

# 5. Start the API server (with auto-reload in development)
python main.py
```

The API will be available at: http://localhost:8000

Interactive API documentation is available at: http://localhost:8000/docs

### Quick Health Check Example

After the server is running, you can verify it with `curl`:

```bash
curl http://localhost:8000/health
```

Expected response (example):

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

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
├── specs/                       # Feature specifications and design docs
├── docs/                        # Project documentation
└── config.yaml                  # Project configuration
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

### Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/prompts` | List all prompts (supports `collection_id` and `search` query params) |
| GET | `/prompts/{id}` | Get single prompt |
| POST | `/prompts` | Create prompt |
| PUT | `/prompts/{id}` | Update prompt |
| PATCH | `/prompts/{id}` | Partially update prompt |
| DELETE | `/prompts/{id}` | Delete prompt |
| GET | `/collections` | List collections |
| GET | `/collections/{id}` | Get collection |
| POST | `/collections` | Create collection |
| DELETE | `/collections/{id}` | Delete collection |

### Models (Simplified)

**Prompt**

```json
{
  "id": "string",
  "title": "string",
  "content": "string",
  "description": "string or null",
  "collection_id": "string or null",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**Collection**

```json
{
  "id": "string",
  "name": "string",
  "description": "string or null",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Example: Create a Prompt (Successful Request)

```bash
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code Review Prompt",
    "content": "Review the following code and provide feedback:\n\n{{code}}",
    "description": "A prompt for AI code review"
  }'
```

Example response:

```json
{
  "id": "1f8f1b44-1c2d-4c1e-9f3d-123456789abc",
  "title": "Code Review Prompt",
  "content": "Review the following code and provide feedback:\n\n{{code}}",
  "description": "A prompt for AI code review",
  "collection_id": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Example: Get a List of Prompts (GET Request)

```bash
curl "http://localhost:8000/prompts"
```

Example response:

```json
{
  "prompts": [
    {
      "id": "1f8f1b44-1c2d-4c1e-9f3d-123456789abc",
      "title": "Code Review Prompt",
      "content": "Review the following code and provide feedback:\n\n{{code}}",
      "description": "A prompt for AI code review",
      "collection_id": null,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

You can filter and search prompts using query parameters:

```bash
# Filter by collection ID
curl "http://localhost:8000/prompts?collection_id=abc123"

# Search in title/description
curl "http://localhost:8000/prompts?search=review"
```

### Example: Error Response (Prompt Not Found)

Requesting a non-existent prompt ID returns a 404 error:

```bash
curl -i http://localhost:8000/prompts/nonexistent-id
```

Example response:

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "detail": "Prompt not found"
}
```

---

## Development Setup

### Local Development

- Use the provided `python main.py` command from the `backend/` directory to run
the FastAPI app locally.
- The server is started with `reload=True` (see `backend/main.py`), so code
  changes in the backend are automatically reloaded during development.

```bash
cd backend
python main.py
```

The server will listen on `http://0.0.0.0:8000`.

### Running Tests

- From the repository root or inside `backend/`, with your virtual environment
  activated, run:

```bash
cd backend
pytest tests/ -v
```

---

## Contributing

We welcome improvements to PromptLab. To keep the project maintainable:

1. **Work on a branch and open a Pull Request (PR)**
   - Create a feature or bugfix branch from `main`.
   - Open a PR describing the changes you are proposing.
2. **Run the test suite before submitting**
   - Ensure `pytest tests/ -v` passes locally before requesting review.
3. **Add tests for bug fixes and new endpoints**
   - When you fix a bug, add or update tests that would fail without the fix.
   - When you add or change an endpoint, include tests that cover the new
     behavior.
4. **Update documentation when API behavior changes**
   - Keep this `README.md` and any related docs in `docs/` and `specs/` in sync
     with the implemented API.

---

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic
- **Frontend**: React, Vite (Week 4)
- **Testing**: pytest
- **DevOps**: Docker, GitHub Actions (Week 3)

---

Good luck, and welcome to the team! 🚀
