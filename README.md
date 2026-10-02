# EXAMMIND - AI-Powered Personalized Study Planner

This project is divided into a React frontend and a FastAPI backend.

## Phase 1: Project Setup & Environment

### Folder Structure

```text
Project Exhibition/
├── EXAMMIND AI Study Planner Exhibition.pptx
├── README.md                 # This file
├── backend/                  # FastAPI Backend
│   ├── .env.example          # Environment variables template for backend
│   ├── requirements.txt      # Python dependencies
│   ├── main.py               # Entry point for FastAPI (to be created in Phase 2)
│   ├── core/                 # Config, security, etc.
│   ├── api/                  # API routes/endpoints
│   ├── services/             # AI, PDF, YouTube service integrations
│   └── models/               # Pydantic models
└── frontend/                 # React + Vite Frontend
    ├── .env.example          # Environment variables template for frontend
    ├── package.json          # Node dependencies
    ├── tailwind.config.js    # Tailwind configuration
    ├── postcss.config.js     # PostCSS configuration
    ├── vite.config.js        # Vite configuration
    ├── public/               # Static assets
    └── src/                  # React source code
        ├── assets/           # Images, icons, etc.
        ├── components/       # Reusable UI components (Shadcn/UI, etc.)
        ├── contexts/         # React Contexts (Auth, etc.)
        ├── hooks/            # Custom React hooks
        ├── lib/              # Utility functions (Firebase init, tailwind merge)
        ├── pages/            # Page components (Dashboard, Login, etc.)
        ├── App.jsx           # Main App component
        └── main.jsx          # Entry point for React
```

### Setup Instructions

#### 1. Backend Setup (FastAPI)
1. Ensure you have Python installed and added to your PATH.
2. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file from the `.env.example`:
   ```bash
   cp .env.example .env
   ```
6. **Populate `.env`**:
   - `FIREBASE_*`: Get these from your Firebase Console (Project Settings -> Service accounts -> Generate new private key).
   - `GEMINI_API_KEY`: Get this from Google AI Studio.
   - `GROQ_API_KEY`: Get this from Groq Console.
   - `YOUTUBE_API_KEY`: Get this from Google Cloud Console (YouTube Data API v3).

#### 2. Frontend Setup (React + Vite)
1. Ensure you have Node.js installed.
2. Open a terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
3. Install dependencies (already started):
   ```bash
   npm install
   ```
4. Create a `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```
5. **Populate `.env`**:
   - `VITE_FIREBASE_*`: Get these from your Firebase Console (Project Settings -> General -> Your apps -> Web app configuration).
   - `VITE_API_BASE_URL`: Leave as `http://localhost:8000` for local development.

### Running the App
- **Backend**: `uvicorn main:app --reload` (inside the `backend` folder with venv activated).
- **Frontend**: `npm run dev` (inside the `frontend` folder).
