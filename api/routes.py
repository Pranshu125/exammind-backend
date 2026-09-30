from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
import shutil
import os
import uuid
from typing import List, Any

from models.schemas import (
    MasterScheduleRequest,

    SyllabusExtractionResponse,
    StudyPlanResponse,
    RevisionNotesResponse,
    QuizResponse,
    VideoResourcesResponse,
    ChatRequest,
    ChatResponse
)
from services.pdf_service import extract_text_from_pdf
from services.ai_service import generate_master_schedule, extract_syllabus_topics, extract_timetable, extract_timetable_from_image, extract_syllabus_from_image, generate_study_plan, generate_revision_notes, generate_quiz
from services.youtube_service import fetch_youtube_videos

router = APIRouter()

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


class SubjectData(BaseModel):
    name: str
    date: str
    time: str
    topics: List[Any]

class MasterScheduleRequest(BaseModel):
    exam_name: str
    subjects: List[SubjectData]
    engine: str = "groq"

class PlanRequest(BaseModel):
    topics: List[Any]
    total_days: int
    engine: str = "groq"

class TopicRequest(BaseModel):
    topic_name: str
    engine: str = "groq"

class QuizRequest(BaseModel):
    topic_name: str
    difficulty: str = "Medium"
    num_questions: int = 3
    engine: str = "groq"

@router.post("/upload", response_model=SyllabusExtractionResponse)
def upload_syllabus(file: UploadFile = File(None), text: str = Form(None), engine: str = Form("groq")):
    try:
        raw_text = ""
        if text:
            structured_data = extract_syllabus_topics(text, engine=engine)
            return SyllabusExtractionResponse(**structured_data)
        elif file:
            allowed_exts = (".pdf", ".jpg", ".jpeg", ".png")
            if not any(file.filename.lower().endswith(ext) for ext in allowed_exts):
                raise HTTPException(status_code=400, detail="Only PDF or Image files are allowed.")
                
            temp_file_path = os.path.join(TEMP_DIR, f"syl_{uuid.uuid4()}_{file.filename}")
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
            if temp_file_path.lower().endswith(".pdf"):
                raw_text = extract_text_from_pdf(temp_file_path)
                
                if len(raw_text.strip()) == 0:
                    import fitz
                    doc = fitz.open(temp_file_path)
                    page = doc.load_page(0)
                    pix = page.get_pixmap()
                    img_bytes = pix.tobytes("png")
                    doc.close()
                    os.remove(temp_file_path)
                    structured_data = extract_syllabus_from_image(img_bytes)
                    return SyllabusExtractionResponse(**structured_data)
                else:
                    os.remove(temp_file_path)
                    structured_data = extract_syllabus_topics(raw_text, engine=engine)
                    return SyllabusExtractionResponse(**structured_data)
            else:
                with open(temp_file_path, "rb") as img_file:
                    img_bytes = img_file.read()
                os.remove(temp_file_path)
                structured_data = extract_syllabus_from_image(img_bytes)
                return SyllabusExtractionResponse(**structured_data)
        else:
            raise HTTPException(status_code=400, detail="Must provide either file or text.")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-plan", response_model=StudyPlanResponse)
def create_plan(request: PlanRequest):
    try:
        plan = generate_study_plan(request.topics, request.total_days, engine=request.engine)
        return StudyPlanResponse(**plan)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-notes", response_model=RevisionNotesResponse)
def create_notes(request: TopicRequest):
    try:
        notes = generate_revision_notes(request.topic_name, engine=request.engine)
        return RevisionNotesResponse(**notes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-quiz", response_model=QuizResponse)
def create_quiz(request: QuizRequest):
    try:
        quiz = generate_quiz(
            request.topic_name, 
            engine=request.engine, 
            difficulty=request.difficulty, 
            num_questions=request.num_questions
        )
        return QuizResponse(**quiz)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fetch-videos", response_model=VideoResourcesResponse)
def get_videos(request: TopicRequest):
    try:
        videos = fetch_youtube_videos(request.topic_name)
        return VideoResourcesResponse(topic_name=request.topic_name, videos=videos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    from services.ai_service import chat_with_notes
    try:
        reply = chat_with_notes(request.messages, request.topic_name, engine=request.engine)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-timetable")
def upload_timetable(file: UploadFile = File(...), engine: str = Form("groq")):
    allowed_exts = (".pdf", ".jpg", ".jpeg", ".png")
    if not any(file.filename.lower().endswith(ext) for ext in allowed_exts):
        raise HTTPException(status_code=400, detail="Only PDF or Image files are allowed.")
        
    temp_file_path = os.path.join(TEMP_DIR, f"tt_{uuid.uuid4()}_{file.filename}")
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        if temp_file_path.lower().endswith(".pdf"):
            raw_text = extract_text_from_pdf(temp_file_path)
            
            if len(raw_text.strip()) == 0:
                # Fallback to Vision extraction using PyMuPDF
                import fitz
                doc = fitz.open(temp_file_path)
                page = doc.load_page(0)  # Use first page
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                doc.close()
                os.remove(temp_file_path)
                
                timetable_data = extract_timetable_from_image(img_bytes)
                return timetable_data
            else:
                os.remove(temp_file_path)
                timetable_data = extract_timetable(raw_text, engine=engine)
                return timetable_data
        else:
            # It's an image
            with open(temp_file_path, "rb") as img_file:
                img_bytes = img_file.read()
            os.remove(temp_file_path)
            timetable_data = extract_timetable_from_image(img_bytes)
            return timetable_data
        
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-master-schedule")
def create_master_schedule(request: MasterScheduleRequest):
    try:
        data = request.model_dump()
        schedule = generate_master_schedule(data, engine='gemini')
        return schedule
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/solve-doubt")
def solve_doubt_endpoint(question: str = Form(...), file: UploadFile = File(None)):
    from services.ai_service import solve_doubt
    try:
        img_bytes = None
        if file:
            img_bytes = file.file.read()
        answer = solve_doubt(question, img_bytes)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
