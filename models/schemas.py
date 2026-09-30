from pydantic import BaseModel
from typing import List, Optional, Any

class Topic(BaseModel):
    id: str
    name: str
    description: str
    estimated_hours: float

class SyllabusExtractionResponse(BaseModel):
    subject: str
    topics: List[Topic]

class StudyDay(BaseModel):
    day: int
    date: Optional[str] = None
    topics_to_cover: List[str]
    tasks: List[str]
    estimated_minutes: int

class StudyPlanResponse(BaseModel):
    plan_title: str
    days: List[StudyDay]

class NoteSection(BaseModel):
    heading: str
    content: str

class RevisionNotesResponse(BaseModel):
    topic_name: str
    sections: List[NoteSection]
    summary: str

class QuizOption(BaseModel):
    label: str # e.g., A, B, C, D
    text: str

class QuizQuestion(BaseModel):
    question: str
    options: List[QuizOption]
    correct_option_label: str
    explanation: str

class QuizResponse(BaseModel):
    topic_name: str
    questions: List[QuizQuestion]

class VideoResource(BaseModel):
    title: str
    video_id: str
    thumbnail_url: str
    channel_title: str

class VideoResourcesResponse(BaseModel):
    topic_name: str
    videos: List[VideoResource]

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    topic_name: str
    engine: str = "groq"

class ChatResponse(BaseModel):
    reply: str

class SubjectData(BaseModel):
    name: str
    date: str
    time: str
    topics: List[Any]

class MasterScheduleRequest(BaseModel):
    exam_name: str
    subjects: List[SubjectData]
    engine: str = "groq"
