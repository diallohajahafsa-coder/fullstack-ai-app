# Fullstack AI App

A beginner-friendly React, Flask, and MongoDB starter. The React app talks to a
Flask JSON API; MongoDB persistence is optional for local development.

## Project structure

```text
backend/
  routes/       API endpoints
  services/     Sentiment analysis logic
  db.py         MongoDB connection and collection access
  tests/        Backend tests
frontend/src/
  components/   Reusable interface components
  pages/        Application screens
  services/     Frontend API client
```

## Requirements

- Node.js 20.19+ or 22.12+
- Python 3.10+
- MongoDB Community or MongoDB Atlas (optional)

## Start the backend

From the project root, create and activate a virtual environment:

```powershell
cd backend
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
flask --app app run --debug --port 5000
```

The backend runs at `http://127.0.0.1:5000`. Check
`http://127.0.0.1:5000/api/health` to see its status.

### Connect MongoDB Atlas

1. In MongoDB Atlas, create a cluster and a **database user**. This is separate
   from your Atlas website login.
2. In **Network Access**, allow your current IP address. Avoid `0.0.0.0/0`
   except for a temporary test when you understand that it allows connections
   from anywhere.
3. In the cluster, choose **Connect → Drivers → Python** and copy the connection
   string.
4. Open `backend/.env` and replace the example `MONGO_URI` with that string.
   Replace the username and password placeholders; URL-encode special
   characters in the password. Keep `/ai_fullstack` as the database name, or
   change it to the database you prefer.
5. Restart Flask and open `http://127.0.0.1:5000/api/health`. A successful
   connection returns `"database": "connected"`.
6. Submit text in the frontend. A successful response says `"stored": true`,
   and Atlas creates the `sentiment_history` collection on the first insert.

Never commit or share `backend/.env` or paste its connection string into chat.
It is ignored by Git. The API reports a database connection failure rather than
pretending a result was saved.

## Start the frontend

In a second terminal, from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (normally `http://localhost:5173`). Vite proxies
`/api` requests to the Flask server. Set `VITE_API_URL` in
`frontend/.env.local` only when the API is hosted at a different address.

## Demo API

- `GET /api/health` — API and database status
- `POST /api/sentiment` — accepts `{"text": "..."}` and returns a demo,
  rules-based sentiment result

The sentiment analyzer is intentionally a small demo, not a trained model.
Replace it with a real model before relying on its predictions.

## Deploy to Render and Vercel

### Backend on Render

1. Create a Render **Blueprint** from this GitHub repository. The root
   `render.yaml` defines the Python web service and its health check.
2. In the Render service's environment settings, set `MONGO_URI` to your Atlas
   connection string and `FRONTEND_ORIGIN` to your deployed Vercel origin.
   Keep `MONGO_URI` in Render's secret environment settings, not in Git.
3. In Atlas **Network Access**, allow the Render service's outbound IP
   addresses. Do not expose the database to all IPs for convenience.
4. After deployment, verify `https://<your-render-service>.onrender.com/api/health`
   reports `"database": "connected"`.

### Frontend on Vercel

1. Import the same GitHub repository into Vercel and set **Root Directory** to
   `frontend`. Use `npm run build` as the build command and `dist` as the output
   directory.
2. Add the environment variable `VITE_API_URL` with the deployed Render API
   base URL, ending in `/api` (for example,
   `https://<your-render-service>.onrender.com/api`).
3. Deploy, then update Render's `FRONTEND_ORIGIN` to the Vercel site's origin
   (for example, `https://<your-project>.vercel.app`) and redeploy/restart the
   Render service so its CORS setting takes effect.

## Tests

With the backend virtual environment active:

```powershell
python -m unittest discover -s tests
```
