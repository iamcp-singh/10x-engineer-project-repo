# PromptLab Deployment Guide

## Prerequisites

- **Python 3.10 or higher**
- **Node.js 18 or higher** and **npm**
- **Git**

---

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/iamcp-singh/10x-engineer-project-repo.git
cd 10x-engineer-project-repo
```

### 2. Start the Backend

Open a terminal window:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend will start at **http://localhost:8000**

### 3. Start the Frontend

Open a **new terminal window**:

```bash
cd frontend
npm install
npm run dev
```

Frontend will start at **http://localhost:5173**

### 4. Access the Application

Open your browser to **http://localhost:5173**

---

## Environment Variables

**No environment variables required.**

- Backend uses in-memory storage
- Frontend connects to `http://localhost:8000` by default

---

## Secrets Handling

**No secrets or credentials are required:**
- No database passwords (in-memory storage)
- No API keys
- No authentication tokens

---

## Verify Deployment

### Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected output:
```json
{"status":"healthy","version":"0.1.0"}
```

### Frontend UI

Open browser to http://localhost:5173 and verify:
- Can create a collection
- Can create a prompt
- Can view prompt details
- Can edit a prompt
- Can delete a prompt (with confirmation)
- Search bar works
- Filter by collection works

---

## Stop the Application

Press **Ctrl+C** in each terminal window to stop the servers.
