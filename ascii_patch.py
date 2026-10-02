import re

with open('services/ai_service.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Replace the generic JSON prompt instructions
code = re.sub(
    r'Include Mermaid\.js markdown blocks \(```mermaid \.\.\. ```\) for diagrams and flowcharts in your explanation ONLY IF needed\.',
    'If you need to include diagrams or flowcharts in your explanation, use raw ASCII art / text-based symbols wrapped in standard markdown code blocks (```text ... ```) instead of Mermaid.',
    code
)

# 2. Replace the specific chat_with_notes system prompt
chat_prompt_old = r'IMPORTANT: When explaining complex concepts, or if the user asks for a diagram, flowchart, or visual, you MUST use Mermaid\.js markdown blocks \(```mermaid \.\.\. ```\)\.\nCRITICAL MERMAID SYNTAX RULES:\n1\. Always start flowcharts with `flowchart TD` or `flowchart LR`\.\n2\. Always use valid arrow syntax: `-->` for solid links, `-\.->` for dotted\. Never use single hyphens like `->`\.\n3\. You MUST wrap ALL node text labels in double quotes, especially if they contain spaces or parentheses\. Example: `A\["Initial Step \(Start\)"\] --> B\["Final Step"\]`\.\n4\. Avoid HTML tags inside Mermaid labels\. Keep diagrams clean and structural\.'

chat_prompt_new = 'IMPORTANT: When explaining complex concepts, or if the user asks for a diagram, flowchart, or visual, you MUST use raw ASCII art / text-based symbols wrapped in standard markdown code blocks (```text ... ```) instead of Mermaid.'

code = re.sub(chat_prompt_old, chat_prompt_new, code)

with open('services/ai_service.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Replaced successfully')
