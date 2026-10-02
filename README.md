# Exammind - AI-Powered Personalized Study Planner 🧠📚

![Exammind Banner](https://via.placeholder.com/1200x300?text=Exammind+-+AI+Study+Planner)

**Exammind** is a next-generation, AI-driven study planner and curriculum tracker built to revolutionize how students prepare for exams. By leveraging advanced Large Language Models (Groq and Google Gemini), Exammind transforms raw syllabus documents and PDFs into highly structured, day-by-day study schedules, interactive revision notes, and self-assessment quizzes.

*Developed for the Project Exhibition.*

---

## ✨ Core Features

### 📅 AI-Powered Timetable Generation
- Upload any syllabus or curriculum document (PDF/Text).
- Our AI engines parse the document and extract key topics.
- Automatically generates a realistic, day-by-day study schedule based on your available study hours.
- Adjustable difficulty and time constraints.

### 📝 Dynamic Revision Notes & Flashcards
- Generate on-demand, highly detailed study material for any specific curriculum topic.
- AI dynamically creates ASCII summaries, key bullet points, and deep-dive explanations.
- **Multi-Model Support:** Switch between Groq (for blazing fast inference) and Gemini (for complex reasoning) directly within the Notes UI.
- Built-in **Token Usage** tracking to monitor API limits.

### 🎯 Interactive Practice Quizzes
- Test your knowledge with AI-generated multiple-choice questions.
- Customizable difficulty levels (Beginner, Medium, Advanced) and question counts.
- Instant feedback with detailed explanations for correct and incorrect answers.

### 🔗 Calendar Auto-Sync (WebCal Integration)
- Seamlessly synchronize your generated timetables with external calendar applications.
- Supports **Google Calendar, Apple Calendar, and Microsoft Outlook**.
- Real-time tracking locks curriculum modules to your local time zone, allowing you to easily see what you need to study "Today".

### 🎥 YouTube Tutorial Finder
- Automatically fetches relevant educational YouTube videos for your specific topics to supplement your reading material.

---

## 🛠️ Technical Architecture

Exammind is built using a modern decoupled architecture, ensuring scalability and responsiveness.

### Frontend (Client-Side)
- **Framework:** React.js powered by Vite
- **Styling:** TailwindCSS for utility-first, responsive design
- **Icons:** Lucide React
- **Hosting & Auth:** Firebase (Authentication, Firestore Database, Firebase Hosting)
- **State Management:** React Context API (AuthContext, AIContext, ThemeContext)

### Backend (API Server)
- **Framework:** FastAPI (Python)
- **AI Integrations:**
  - **Groq API** (`openai/gpt-oss-20b` equivalent) for fast inference.
  - **Google Generative AI (Gemini)** for deep reasoning.
- **Document Processing:** PyPDF2 for syllabus extraction.
- **Data Validation:** Pydantic schemas.
- **Hosting:** Render (Cloud Application Hosting)

---

## 🚀 Setup & Installation

Follow these instructions to run Exammind locally on your machine.

### Prerequisites
- Node.js (v16+)
- Python (3.9+)
- Firebase Account (for Auth and Database)
- API Keys (Groq, Google Gemini, YouTube Data API v3)

### 1. Backend Setup (FastAPI)

1. Clone the repository and navigate to the backend directory:
   ```bash
   git clone https://github.com/Pranshu125/exammind-backend.git
   cd exammind-backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root backend directory and add your API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   YOUTUBE_API_KEY=your_youtube_api_key_here
   FIREBASE_CREDENTIALS=...
   ```
5. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```
   *The API will be available at `http://localhost:8000`.*

### 2. Frontend Setup (React + Vite)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the required Node dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file in the `frontend` directory and add your Firebase configuration:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_FIREBASE_API_KEY=your_firebase_api_key
   VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   VITE_FIREBASE_PROJECT_ID=your_project_id
   VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
   VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   VITE_FIREBASE_APP_ID=your_app_id
   ```
4. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend will be available at `http://localhost:5173`.*

---

## 📅 WebCal Sync Instructions
To sync your Exammind timetable with your calendar:
1. Navigate to the **Settings** page in the dashboard.
2. Click **Configure & Sync** under the Calendar Integration section.
3. Copy the provided WebCal URL (`webcal://...`).
4. Paste the URL into your calendar provider:
   - **Google Calendar:** Settings -> Add Calendar -> From URL
   - **Apple Calendar:** File -> New Calendar Subscription
   - **Outlook:** Add Calendar -> Subscribe from web

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Pranshu125/exammind-backend/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
*Built with ❤️ for the Future of Education.*
