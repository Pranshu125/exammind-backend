import json
from datetime import datetime
import google.generativeai as genai
from openai import OpenAI
from core.config import settings
import io
from PIL import Image

# API Key Rotation Logic
current_groq_index = 0
current_gemini_index = 0

def get_groq_client():
    global current_groq_index
    from groq import Groq
    if not settings.GROQ_KEYS: return None
    return Groq(api_key=settings.GROQ_KEYS[current_groq_index])

def rotate_groq():
    global current_groq_index
    if settings.GROQ_KEYS:
        current_groq_index = (current_groq_index + 1) % len(settings.GROQ_KEYS)
        print(f"Rotated Groq Key to index {current_groq_index}")

def configure_gemini():
    global current_gemini_index
    if settings.GEMINI_KEYS:
        genai.configure(api_key=settings.GEMINI_KEYS[current_gemini_index])

def rotate_gemini():
    global current_gemini_index
    if settings.GEMINI_KEYS:
        current_gemini_index = (current_gemini_index + 1) % len(settings.GEMINI_KEYS)
        configure_gemini()
        print(f"Rotated Gemini Key to index {current_gemini_index}")

configure_gemini()

deepseek_client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com") if settings.DEEPSEEK_API_KEY else None

def call_ai_engine(prompt: str, engine: str = "gemini") -> str:
    import re
    if engine == "groq":
        for _ in range(max(1, len(settings.GROQ_KEYS))):
            try:
                groq_client = get_groq_client()
                if not groq_client: raise ValueError("Groq API Key missing")
                safe_prompt = prompt + "\n\nCRITICAL: You MUST return ONLY a valid JSON object. DO NOT include raw unescaped backslashes (like \\n or \\rightarrow). Use standard valid JSON escaping."
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    response_format={"type": "json_object"},
                    messages=[{"role": "user", "content": safe_prompt}],
                    max_tokens=6000
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Groq error: {e}")
                rotate_groq()
        raise ValueError("All Groq keys failed.")
        
    elif engine.startswith("ollama"):
        local_model = engine.split("-")[1] if "-" in engine else "qwen2.5:14b"
        try:
            ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
            response = ollama_client.chat.completions.create(model=local_model, messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Ollama connection failed for {local_model}. Ensure Ollama is running. Error: {e}")

    else: # gemini
        for _ in range(max(1, len(settings.GEMINI_KEYS))):
            try:
                model = genai.GenerativeModel('gemini-3.5-flash')
                response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                return response.text
            except Exception as e:
                print(f"Gemini error: {e}")
                rotate_gemini()
        raise ValueError("All Gemini keys failed.")


def generate_study_plan(topics: list, total_days: int, engine: str = "groq") -> dict:
    prompt = f'''
    Create a {total_days}-day study plan for these topics: {json.dumps(topics)}.
    Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
    {{
        "total_days": {total_days},
        "daily_plan": [
            {{
                "day": 1,
                "focus": "Topic 1",
                "tasks": ["Task A", "Task B"]
            }}
        ]
    }}
    Ensure exactly {total_days} days are generated.
    '''
    raw_response = call_ai_engine(prompt, engine)
    clean_response = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean_response)


def generate_revision_notes(topic: str, engine: str = "groq") -> dict:
    prompt = f'''
    Generate highly detailed, educational revision notes for the topic: '{topic}'.
    Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
    {{
        "topic_name": "{topic}",
        "sections": [
            {{
                "heading": "Heading Name",
                "content": "Detailed markdown formatted text here..."
            }}
        ]
    }}
    '''
    raw_response = call_ai_engine(prompt, engine)
    clean_response = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean_response)


def generate_quiz(topic: str, difficulty: str = "Medium", num_questions: int = 5, engine: str = "groq") -> dict:
    prompt = f'''
    Create a {difficulty} difficulty multiple choice quiz about '{topic}' with exactly {num_questions} questions.
    Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
    {{
        "topic_name": "{topic}",
        "questions": [
            {{
                "question": "Question text?",
                "options": [
                    {{"label": "A", "text": "Option A"}},
                    {{"label": "B", "text": "Option B"}},
                    {{"label": "C", "text": "Option C"}},
                    {{"label": "D", "text": "Option D"}}
                ],
                "correct_option_label": "A",
                "explanation": "Why it is correct"
            }}
        ]
    }}
    Ensure there are exactly {num_questions} questions.
    '''
    raw_response = call_ai_engine(prompt, engine)
    clean_response = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean_response)

def chat_with_notes(messages: list, topic: str, engine: str = "gemini") -> str:
    system_prompt = f"""You are an expert AI study tutor for the topic: '{topic}'. Keep answers concise and highly educational.
IMPORTANT: When explaining complex concepts, or if the user asks for a diagram, flowchart, or visual, you MUST use Mermaid.js markdown blocks (```mermaid ... ```).
CRITICAL MERMAID SYNTAX RULES:
1. Always start flowcharts with `flowchart TD` or `flowchart LR`.
2. Always use valid arrow syntax: `-->` for solid links, `-.->` for dotted. Never use single hyphens like `->`.
3. You MUST wrap ALL node text labels in double quotes, especially if they contain spaces or parentheses. Example: `A["Initial Step (Start)"] --> B["Final Step"]`.
4. Avoid HTML tags inside Mermaid labels. Keep diagrams clean and structural."""
    
    formatted_messages = [{"role": "system", "content": system_prompt}]
    for msg in messages:
        formatted_messages.append({"role": msg.role, "content": msg.content})

    if engine == "groq":
        for _ in range(max(1, len(settings.GROQ_KEYS))):
            try:
                groq_client = get_groq_client()
                if not groq_client: raise ValueError("Groq API Key missing")
                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=formatted_messages
                )
                return response.choices[0].message.content
            except Exception as e:
                rotate_groq()
        raise ValueError("All Groq keys failed")

    elif engine.startswith("ollama"):
        local_model = engine.split("-")[1] if "-" in engine else "qwen2.5:14b"
        try:
            ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
            response = ollama_client.chat.completions.create(model=local_model, messages=formatted_messages)
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Ollama connection failed for {local_model}. Ensure Ollama is running. Error: {e}")

    else: # gemini
        for _ in range(max(1, len(settings.GEMINI_KEYS))):
            try:
                model = genai.GenerativeModel('gemini-3.5-flash')
                gemini_history = [{"role": "user", "parts": [system_prompt + "\\n\\nAcknowledge this and wait for my query."]}, {"role": "model", "parts": ["Understood! How can I help you?"]}]
                for msg in messages:
                    gemini_history.append({"role": "user" if msg.role == "user" else "model", "parts": [msg.content]})
                
                if len(gemini_history) > 0 and gemini_history[-1]["role"] == "user":
                    prompt_text = gemini_history.pop()["parts"][0]
                else:
                    prompt_text = "Continue"
                    
                chat = model.start_chat(history=gemini_history)
                response = chat.send_message(prompt_text)
                return response.text
            except Exception as e:
                rotate_gemini()
        raise ValueError("All Gemini keys failed")

def extract_timetable(timetable_text: str, engine: str = "groq") -> dict:
    prompt = f'''
    Analyze the following exam timetable text and extract a list of exams. 
    Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
    {{
        "exam_name": "Name of the overarching exam period (e.g. CAT 2, Midterms)",
        "subjects": [
            {{
                "id": 1,
                "name": "Subject Name",
                "date": "YYYY-MM-DD",
                "time": "HH:MM"
            }}
        ]
    }}
    
    Timetable Text:
    {timetable_text[:8000]}
    '''
    raw_response = call_ai_engine(prompt, engine)
    clean_response = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean_response)

def extract_timetable_from_image(image_bytes: bytes) -> dict:
    for _ in range(max(1, len(settings.GEMINI_KEYS))):
        try:
            model = genai.GenerativeModel('gemini-3.5-flash')
            image = Image.open(io.BytesIO(image_bytes))
            prompt = '''
            Analyze the following exam timetable image and extract a list of exams. 
            Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
            {
                "exam_name": "Name of the overarching exam period (e.g. CAT 2, Midterms)",
                "subjects": [
                    {
                        "id": 1,
                        "name": "Subject Name",
                        "date": "YYYY-MM-DD",
                        "time": "HH:MM"
                    }
                ]
            }
            '''
            response = model.generate_content([prompt, image], generation_config={"response_mime_type": "application/json"})
            clean_response = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return json.loads(clean_response)
        except Exception as e:
            rotate_gemini()
    raise ValueError("All Gemini keys failed")

def extract_syllabus_from_image(image_bytes: bytes) -> dict:
    for _ in range(max(1, len(settings.GEMINI_KEYS))):
        try:
            model = genai.GenerativeModel('gemini-3.5-flash')
            image = Image.open(io.BytesIO(image_bytes))
            prompt = '''
            Analyze the following syllabus image and extract a list of core study topics. 
            Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
            {
                "subject": "Name of the subject (infer if possible)",
                "topics": [
                    {
                        "id": "unique-id-1",
                        "name": "Topic Name",
                        "description": "Brief description",
                        "estimated_hours": 2.5
                    }
                ]
            }
            '''
            response = model.generate_content([prompt, image], generation_config={"response_mime_type": "application/json"})
            clean_response = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return json.loads(clean_response)
        except Exception as e:
            rotate_gemini()
    raise ValueError("All Gemini keys failed")

def generate_master_schedule(exam_data: dict, engine: str = "groq") -> dict:
    prompt = f'''
    You are an expert AI study planner. I will provide you with an exam period name and a list of subjects.
    For each subject, I will provide the exam date and time, and the core topics that need to be studied.
    
    Your task is to create a realistic, balanced, and optimized daily study schedule starting from TODAY until the last exam date.
    Allocate time dynamically based on the "estimated_hours" or size of each topic, prioritizing subjects whose exams are sooner.
    Ensure topics are spread out reasonably.
    
    Here is the data:
    {json.dumps(exam_data, indent=2)}
    
    Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
    {{
        "exam_name": "Name of the exam (e.g. CAT 2)",
        "created_at": "YYYY-MM-DD",
        "schedule": [
            {{
                "date": "YYYY-MM-DD",
                "day_of_week": "Monday",
                "tasks": [
                    {{
                        "subject": "Subject Name",
                        "topic": "Topic Name",
                        "task_type": "Study" | "Revision" | "Practice",
                        "duration_minutes": 120,
                        "completed": false
                    }}
                ]
            }}
        ]
    }}
    '''
    raw_response = call_ai_engine(prompt, engine)
    clean_response = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean_response)

def solve_doubt(question: str, image_bytes: bytes = None) -> str:
    for _ in range(max(1, len(settings.GEMINI_KEYS))):
        try:
            model = genai.GenerativeModel('gemini-3.5-flash')
            if image_bytes:
                img = Image.open(io.BytesIO(image_bytes))
                response = model.generate_content([question, img])
            else:
                response = model.generate_content(question)
            return response.text
        except Exception as e:
            rotate_gemini()
    return "Error: All Gemini keys failed."

def extract_syllabus_topics(text: str, engine: str = "groq") -> dict:
    prompt = f'''
    Analyze the following syllabus text and extract a list of core study topics. 
    Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
    {{
        "subject": "Name of the subject (infer if possible)",
        "topics": [
            {{
                "id": "unique-id-1",
                "name": "Topic Name",
                "description": "Brief description",
                "estimated_hours": 2.5
            }}
        ]
    }}
    
    Syllabus Text:
    {text[:8000]}
    '''
    raw_response = call_ai_engine(prompt, engine)
    clean_response = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean_response)
