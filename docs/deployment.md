# PromptLab Deployment Guide

This guide provides complete instructions to run the PromptLab application.

## Prerequisites

- **Python 3.10 or higher** installed
- **Node.js 18 or higher** and **npm** installed
- **Git** installed

---

## Quick Start (Run in 3 Minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/iamcp-singh/10x-engineer-project-repo.git
cd 10x-engineer-project-repo
```

### 2. Start the Backend (Terminal 1)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend will start at **http://localhost:8000**

### 3. Start the Frontend (Terminal 2)

Open a **new terminal window**:

```bash
cd frontend
npm install
npm run dev
```

Frontend will start at **http://localhost:5173**

### 4. Access the Application

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Health Check**: http://localhost:8000/health

---

## What's Running

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| **backend** | 8000 | http://localhost:8000 | FastAPI backend with in-memory storage |
| **frontend** | 5173 | http://localhost:5173 | React UI with Vite dev server |

---

## Environment Variables

### Backend
- **No environment variables required**
- Uses in-memory storage (data clears on restart)

### Frontend
- `VITE_API_URL`: Backend API URL
  - Default: `http://localhost:8000` (configured in `frontend/src/api/client.js`)
  - To change: Create `frontend/.env.local` with `VITE_API_URL=your-backend-url`

---

## Testing the Deployment

### 1. Verify Backend is Running

```bash
# Health check
curl http://localhost:8000/health

# Expected output:
# {"status":"healthy","version":"0.1.0"}

# List prompts (empty initially)
curl http://localhost:8000/prompts

# Expected output:
# {"prompts":[],"total":0}
```

### 2. Verify Frontend is Running

Open browser to: http://localhost:5173

You should see the PromptLab interface.

### 3. Test Full CRUD Flow

1. **Create a Collection:**
   - Click "New Collection"
   - Name: "Test Collection"
   - Description: "My first collection"
   - Click "Create Collection"

2. **Create a Prompt:**
   - Click "New Prompt"
   - Title: "Test Prompt"
   - Content: "You are a helpful assistant"
   - Tags: "test, ai"
   - Click "Create"

3. **View Prompt:**
   - Click on the prompt card
   - Verify details are shown correctly

4. **Edit Prompt:**
   - Click "Edit"
   - Change title to "Updated Prompt"
   - Click "Update"

5. **Delete Prompt:**
   - Click "Delete"
   - Confirm deletion
   - Verify prompt is removed

6. **Search:**
   - Create multiple prompts
   - Use search bar to filter

7. **Filter by Collection:**
   - Click collection in sidebar
   - Verify only prompts in that collection show

---

## Running Backend Tests

To verify all tests pass (required for C3.2):

### With Backend Running

```bash
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pytest tests/ -v
```

**Expected**: All 80 tests should pass.

---

## Stopping the Application

- In each terminal window, press **Ctrl+C** to stop the server
- Backend and frontend can be stopped independently

---

## Troubleshooting

### Port Already in Use

**Problem:** Error like `Address already in use` on port 8000 or 5173

**Solution:**
```bash
# Find what's using the port
lsof -ti:8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill <process_id>
```

### Frontend Shows "Failed to Fetch"

**Problem:** Frontend can't connect to backend

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `VITE_API_URL` in `frontend/src/api/client.js` (default: `http://localhost:8000`)
3. Clear browser cache and refresh

### Python Version Mismatch

**Problem:** Syntax errors or import errors

**Solution:**
```bash
# Check Python version
python --version  # Must be 3.10 or higher

# If too old, install Python 3.10+ and use:
python3.10 -m venv .venv
```

---

## Secrets Handling

**This project has no secrets or credentials:**
- No database passwords (using in-memory storage)
- No API keys (no third-party integrations)
- No authentication tokens

The `.env.local` file (if created) is gitignored and never committed.

---

## File Structure

```
10x-engineer-project-repo/
├── backend/
│   ├── main.py               # Backend entry point
│   ├── requirements.txt      # Python dependencies
│   ├── app/                  # FastAPI application
│   └── tests/                # Test suite (80 tests)
├── frontend/
│   ├── package.json          # Node dependencies
│   ├── src/                  # React application
│   └── vite.config.js        # Vite configuration
└── docs/
    └── deployment.md         # This file
```

---

## Deployment Checklist

Before submitting, verify:

- [ ] Backend starts without errors: `cd backend && python main.py`
- [ ] Frontend starts without errors: `cd frontend && npm run dev`
- [ ] Backend health endpoint returns 200: `curl http://localhost:8000/health`
- [ ] Frontend loads at http://localhost:5173
- [ ] Can create a collection via UI
- [ ] Can create a prompt via UI
- [ ] Can view prompt details
- [ ] Can edit a prompt
- [ ] Can delete a prompt with confirmation
- [ ] Search works
- [ ] Filter by collection works
- [ ] Backend tests pass: `pytest tests/ -v` (80 tests)
- [ ] No secrets committed to Git
- [ ] Documentation is complete and accurate

---

## Support

For issues:
1. Verify Python 3.10+ is installed: `python --version`
2. Verify Node.js 18+ is installed: `node --version`
3. Ensure ports 5173 and 8000 are free
4. Check backend logs in Terminal 1
5. Check frontend logs in Terminal 2
6. Try reinstalling dependencies:
   - Backend: `pip install -r requirements.txt`
   - Frontend: `rm -rf node_modules && npm install`
