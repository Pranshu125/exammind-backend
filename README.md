# Exammind: AI Study Planner

Exammind is an intelligent study planner and curriculum tracker that leverages advanced AI (Groq & Gemini) to generate comprehensive, optimized study schedules and revision notes from raw syllabi. 

## Features
- **AI-Powered Timetables:** Upload any syllabus document and generate a structured, day-by-day study plan automatically.
- **Dynamic Revision Notes:** Generate on-demand study material and ASCII summaries for any curriculum topic using LLMs.
- **Calendar Auto-Sync (WebCal):** Seamlessly synchronize your generated timetables with Google Calendar, Apple Calendar, and Outlook in the background.
- **Real-Time Tracking:** Lock curriculum modules to your local time zone and easily see what you need to study "Today".
- **Multi-Model Support:** Choose between Groq (Fast) and Gemini (Complex logic) as your preferred AI engine, or plug in your own API keys to bypass rate limits.

## Architecture
- **Backend:** FastAPI (Python), PyPDF2, Pydantic, Groq API, Google GenAI API.
- **Frontend:** React, Vite, TailwindCSS, Firebase (Auth/Firestore/Hosting).
- **Deployment:** Render (Backend) and Firebase Hosting (Frontend).

## Setup & Installation

### Backend
1. Navigate to the root directory.
2. Install dependencies: pip install -r requirements.txt
3. Run the development server: uvicorn main:app --reload

### Frontend
1. Navigate to the frontend directory.
2. Install packages: npm install
3. Run the development environment: npm run dev

---
*Developed for Project Exhibition.*
