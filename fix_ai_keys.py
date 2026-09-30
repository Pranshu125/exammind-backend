import re

with open('services/ai_service.py', 'r') as f:
    code = f.read()

rotation_logic = """
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
    import google.generativeai as genai
    if settings.GEMINI_KEYS:
        genai.configure(api_key=settings.GEMINI_KEYS[current_gemini_index])

def rotate_gemini():
    global current_gemini_index
    if settings.GEMINI_KEYS:
        current_gemini_index = (current_gemini_index + 1) % len(settings.GEMINI_KEYS)
        configure_gemini()
        print(f"Rotated Gemini Key to index {current_gemini_index}")

configure_gemini()
"""

code = re.sub(r'groq_client = Groq\([\s\S]*?else None', rotation_logic, code)
code = re.sub(r'if settings\.GEMINI_API_KEY:\s*genai\.configure\(api_key=settings\.GEMINI_API_KEY\)', '', code)

call_engine_replacement = """
def call_ai_engine(prompt: str, engine: str = "gemini") -> str:
    import re
    reply = ""

    if engine == "groq":
        for _ in range(max(1, len(settings.GROQ_KEYS))):
            try:
                groq_client = get_groq_client()
                if not groq_client: raise ValueError("Groq API Key missing")
                safe_prompt = prompt + "\\n\\nCRITICAL: You MUST return ONLY a valid JSON object. DO NOT include raw unescaped backslashes (like \\\\n or \\\\rightarrow). Use standard valid JSON escaping."
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
"""
code = re.sub(r'def call_ai_engine.*?(?=\n    elif engine\.startswith\("ollama"\):)', call_engine_replacement, code, flags=re.DOTALL)

gemini_replacement = """
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
"""
code = re.sub(r'    else: # gemini.*?return response\.text', gemini_replacement, code, flags=re.DOTALL)

chat_groq_repl = """
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
"""
code = re.sub(r'    if engine == "groq":\n        if not groq_client.*?\n        return response\.choices\[0\]\.message\.content', chat_groq_repl, code, flags=re.DOTALL)

chat_gemini_repl = """
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
"""
code = re.sub(r'    else: # gemini\n        model = genai\.GenerativeModel.*?return response\.text', chat_gemini_repl, code, flags=re.DOTALL)

# Let's fix extract_timetable_from_image, extract_syllabus_from_image, and solve_doubt to also loop gemini
# But since they aren't complex, we can just replace the model call
vision_repl = """
    for _ in range(max(1, len(settings.GEMINI_KEYS))):
        try:
            model = genai.GenerativeModel('gemini-3.5-flash')
            image = Image.open(io.BytesIO(image_bytes))
            response = model.generate_content([prompt, image], generation_config={"response_mime_type": "application/json"})
            clean_response = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return json.loads(clean_response)
        except Exception as e:
            rotate_gemini()
    raise ValueError("All Gemini keys failed")
"""
code = re.sub(r'    model = genai\.GenerativeModel.*?return json\.loads\(clean_response\)', vision_repl, code, flags=re.DOTALL)

# solve_doubt
solve_repl = """
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
"""
code = re.sub(r'    try:\n        model = genai\.GenerativeModel.*?return f"Error: \{str\(e\)\}"', solve_repl, code, flags=re.DOTALL)


with open('services/ai_service.py', 'w') as f:
    f.write(code)

print("Patch applied successfully!")
