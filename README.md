# Hackathon Template: React + Flask

A starter for hackathons: a **Vite + React** frontend and a **Flask** backend in one repo, set up so you can start building features right away.

- **Development:** Vite proxies every `/api` request to Flask, so there's no CORS setup.
- **Production:** Flask serves the built React app *and* the API from a single origin, so you deploy one service.

The same frontend code (`fetch("/api/...")`) works in both, with no hardcoded URLs.

## Project Structure

```
hackathon-template/
├── client/              # Vite + React frontend
│   ├── src/
│   │   ├── api.js       # fetch helper, use this for all API calls
│   │   └── App.jsx
│   └── vite.config.js   # dev proxy: /api → localhost:5001
├── server/              # Flask backend
│   ├── app.py           # API routes + serves the React build
│   ├── requirements.txt
│   └── .env.example     # copy to .env and fill in keys
└── package.json         # root scripts to run everything at once
```

## Prerequisites

- **Node.js** 20+
- **Python** 3.10+ (on Windows, install it from python.org and check **"Add python.exe to PATH"**)

## Setup

### 1. Get the code

Click **"Use this template"** on GitHub, then clone your new repo.

### 2. Backend

**Windows (PowerShell):**

```powershell
cd server
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

**macOS / Linux:**

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 3. Frontend and root tools

From the repo root:

```bash
npm install
cd client && npm install
```

## Running in Development

With the venv **activated**, run this from the repo root:

```bash
npm run dev
```

This starts both servers together, with color-coded logs:

| Service | URL                     |
|---------|-------------------------|
| React   | http://localhost:5173   |
| Flask   | http://localhost:5001   |

Open **localhost:5173**. The page should show **"Backend: ok"**. Vite hot-reloads the frontend, and Flask's debug mode reloads the backend when you save.

## Adding an API Route

1. Add the route in `server/app.py`. **Every route must start with `/api/`**:

   ```python
   @app.get("/api/items")
   def get_items():
       return jsonify(items=[])
   ```

   Define API routes **above** the React catch-all route at the bottom of the file.

2. Call it from React with the helper. Pass only the path **after** `/api`, starting with a slash:

   ```jsx
   import { api } from "./api";

   const data = await api("/items");                // GET /api/items
   await api("/items", {                            // POST /api/items
     method: "POST",
     body: JSON.stringify({ name: "new item" }),
   });
   ```

   The helper throws an error for any non-2xx response, so `.catch()` / `try-catch` receives server errors as well as network failures.

## Environment Variables

- Secrets go in `server/.env`, which **is never committed**. List the key *names* in `.env.example` so teammates know what they need.
- Read them in Flask with `os.getenv("MY_API_KEY")`.
- **Keep API keys in Flask, not React.** Anything in the frontend ships to the browser. Vite only exposes variables prefixed with `VITE_`, and only for values that are safe to make public.

## Testing the Production Build Locally

```bash
npm run build          # builds React into client/dist
cd server
python app.py          # Flask now serves the built app
```

Open **localhost:5001** (not 5173). If "Backend: ok" appears, the production setup works.

> **Remember:** Flask serves the *built* files. After frontend changes, run `npm run build` again before testing on port 5001. During normal development, just use `npm run dev` on port 5173.

## Deploying (Render)

Create **one Web Service** connected to your repo:

| Setting       | Value                                                         |
|---------------|---------------------------------------------------------------|
| Build command | `npm run build && pip install -r server/requirements.txt`     |
| Start command | `cd server && gunicorn app:app`                               |

Add your `.env` values under **Environment** in the Render dashboard.

## Windows Notes

- **`python3` not found:** On Windows, use `py` or `python`. The `python3` command is a Microsoft Store shortcut.
- **"Running scripts is disabled on this system":** Run this once, then activate again:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```
- **Venv paths:** Windows uses `.venv\Scripts\`, and macOS/Linux use `.venv/bin/`.
- **Gunicorn doesn't run on Windows** (it's Unix-only). That's fine, because Render runs Linux. Test production locally with `python app.py` instead.
- **`requirements.txt` looks like binary on GitHub:** Older PowerShell saved it as UTF-16. Regenerate it:
  ```powershell
  pip freeze | Out-File -Encoding utf8 requirements.txt
  ```

## Troubleshooting

| Symptom | Cause / Fix |
|---------|-------------|
| `Backend: error: 404 Not Found` | The request URL doesn't match a Flask route. Check the Flask terminal log for the exact URL. Watch for a doubled prefix (`/api/api/...`) or a double slash (`/api//...`). |
| `No module named flask` | The venv isn't activated in the terminal where you ran `npm run dev`. |
| `Unexpected token '<'` in the browser console | An API call got `index.html` back instead of JSON, which usually means the path doesn't start with `/api/`. |
| Port 5000 already in use (macOS) | AirPlay Receiver uses port 5000. That's why this template uses 5001. |
| Frontend change doesn't show on port 5001 | Run `npm run build` again, because Flask serves the built files. |

## Tech Stack

React · Vite · ESLint · Flask · python-dotenv · Gunicorn · concurrently
