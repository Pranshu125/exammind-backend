import json
import google.generativeai as genai
from openai import OpenAI
from groq import Groq
from core.config import settings

# Initialize Clients
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
openai_client = OpenAI(
    api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
deepseek_client = OpenAI(api_key=settings.DEEPSEEK_API_KEY,
                         base_url="https://api.deepseek.com") if settings.DEEPSEEK_API_KEY else None
groq_client = Groq(
    api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None


def call_ai_engine(prompt: str, engine: str = "gemini") -> str:
    """Routes the prompt to the selected AI engine and returns the raw string response."""
    import re
    reply = ""

    if engine == "groq":
        if not groq_client: raise ValueError("Groq API Key missing")
        safe_prompt = prompt + \
            "\n\nCRITICAL: You MUST return ONLY a valid JSON object. DO NOT include raw unescaped backslashes (like \\n or \\rightarrow). Use standard valid JSON escaping."
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": safe_prompt}],
            max_tokens=6000
        )
        reply = response.choices[0].message.content

    elif engine.startswith("ollama"):
        local_model = engine.split("-")[1] if "-" in engine else "qwen2.5:14b"
        try:
            ollama_client = OpenAI(
                base_url="http://localhost:11434/v1", api_key="ollama")
            response = ollama_client.chat.completions.create(
                model=local_model,
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            raise ValueError(
                f"Ollama connection failed for {local_model}. Ensure Ollama is running. Error: {e}")

    else:  # gemini
        if not gemini_client: raise ValueError("Gemini API Key missing")
        model = gemini_client.GenerativeModel("gemini-3.5-flash")
        response = model.generate_content(prompt)
        reply = response.text

    # Strip markdown code blocks
    if "```" in reply:
        reply = re.sub(r'```(?:json)?', '', reply).strip()
    return reply


def generate_study_plan(topics: list, total_days: int, engine: str = "gemini") -> dict:
    prompt = f"""
    Create a {total_days}-day study plan covering the following topics: {', '.join(topics)}.
    Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
    {{
        "plan_title": "Study Plan Title",
        "days": [
            {{
                "day": 1,
                "topics_to_cover": ["Topic 1"],
                "tasks": ["Read chapter 1", "Practice problems"],
                "estimated_minutes": 120
            }}
        ]
    }}
    Ensure exactly {total_days} days are generated.
    """
    raw_response = call_ai_engine(prompt, engine)
    clean_response = raw_response.strip().removeprefix(
        "```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean_response)

def generate_revision_notes(topic: str, engine: str = "gemini") -> dict:
    prompt = f"""
    Create detailed revision notes for the topic: '{topic}'.
    Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
    {{
        "topic_name": "{topic}",
        "sections": [
            {{
                "heading": "Section Heading",
                "content": "Detailed explanation of this section"
            }}
        ],
        "summary": "High-level summary of the entire topic."
    }}
    """
    raw_response = call_ai_engine(prompt, engine)
    clean_response = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean_response)

def generate_quiz(topic: str, engine: str = "gemini", difficulty: str = "Medium", num_questions: int = 3) -> dict:
    prompt = f"""
    Create a {num_questions}-question multiple choice quiz for the topic: '{topic}'.
    The difficulty level of the questions should be: {difficulty}.
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
    """
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
        if not groq_client: raise ValueError("Groq API Key missing")
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b", # Better chat model for Groq
            messages=formatted_messages
        )
        return response.choices[0].message.content
        
    elif engine.startswith("ollama"):
        local_model = engine.split("-")[1] if "-" in engine else "qwen2.5:14b"
        try:
            ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
            response = ollama_client.chat.completions.create(
                model=local_model,
                messages=formatted_messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Ollama connection failed for {local_model}. Ensure Ollama is running. Error: {e}")
        
    else: # gemini
        model = genai.GenerativeModel('gemini-3.5-flash')
        # Gemini structure expects list of dicts with role=user/model and parts=[...]
        # Plus system instructions if supported, or just prepend to first message
        gemini_history = []
        gemini_history.append({"role": "user", "parts": [system_prompt + "\n\nAcknowledge this and wait for my query."]})
        gemini_history.append({"role": "model", "parts": ["Understood! How can I help you?"]})
        
        for msg in messages:
            role = "user" if msg.role == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg.content]})
            
        # The last message is usually the new user prompt, pop it to use as the actual prompt
        if len(gemini_history) > 0 and gemini_history[-1]["role"] == "user":
            prompt = gemini_history.pop()["parts"][0]
        else:
            prompt = "Continue"
            
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(prompt)
        return response.text


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
    import json
    return json.loads(clean_response)


def extract_timetable_from_image(image_bytes: bytes) -> dict:
    import io
    from PIL import Image
    import google.generativeai as genai
    import json
    
    # We force Gemini 1.5 Flash for vision tasks, as Groq lacks vision in our setup
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    prompt = '''
    Analyze the following exam timetable image and extract a list of exams. 
    Include Mermaid.js markdown blocks (```mermaid ... ```) for diagrams and flowcharts in your explanation ONLY IF needed. Return ONLY a JSON object exactly matching this schema:
    {
        "exam_name": "Name of the overarching exam period (e.g. CAT 2, Midterms, etc)",
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
    
    image = Image.open(io.BytesIO(image_bytes))
    response = model.generate_content([prompt, image], generation_config={"response_mime_type": "application/json"})
    
    clean_response = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean_response)


def extract_syllabus_from_image(image_bytes: bytes) -> dict:
    import io
    from PIL import Image
    import google.generativeai as genai
    import json
    
    model = genai.GenerativeModel('gemini-3.5-flash')
    
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
    
    image = Image.open(io.BytesIO(image_bytes))
    response = model.generate_content([prompt, image], generation_config={"response_mime_type": "application/json"})
    
    clean_response = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(clean_response)


def generate_master_schedule(exam_data: dict, engine: str = "groq") -> dict:
    import json
    from datetime import datetime
    
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
    import google.generativeai as genai
    import io
    from PIL import Image
    
    try:
        model = genai.GenerativeModel('gemini-3.5-flash')
        if image_bytes:
            img = Image.open(io.BytesIO(image_bytes))
            response = model.generate_content([question, img])
        else:
            response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

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
    import json
    return json.loads(clean_response)
