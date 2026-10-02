with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: Full Notes Markdown
old1 = '<ReactMarkdown components={MarkdownComponents} className="prose dark:prose-invert max-w-none prose-sm">{content.notes}</ReactMarkdown>'
new1 = '<div className="prose dark:prose-invert max-w-none prose-sm"><ReactMarkdown components={MarkdownComponents}>{content.notes}</ReactMarkdown></div>'
content = content.replace(old1, new1)

# Fix 2: Chat Messages Markdown
old2 = '<ReactMarkdown components={MarkdownComponents} className="prose dark:prose-invert max-w-none prose-sm">{msg.content}</ReactMarkdown>'
new2 = '<div className="prose dark:prose-invert max-w-none prose-sm"><ReactMarkdown components={MarkdownComponents}>{msg.content}</ReactMarkdown></div>'
content = content.replace(old2, new2)

old3 = "<ReactMarkdown components={MarkdownComponents} className={msg.role === 'user' ? 'text-white' : 'prose dark:prose-invert prose-sm max-w-none'}>"
# Actually I don't think I used this ternary, let's check
if old3 in content:
    print("Found old3")
else:
    print("Not found old3")
    
# Let's just blindly replace any <ReactMarkdown components={MarkdownComponents} className="..."> with wrapper div using regex
import re
def replacer(match):
    cls = match.group(1)
    inner = match.group(2)
    return f'<div className="{cls}"><ReactMarkdown components={{MarkdownComponents}}>{inner}</ReactMarkdown></div>'

content = re.sub(r'<ReactMarkdown components=\{MarkdownComponents\} className="([^"]+)">([\s\S]*?)</ReactMarkdown>', replacer, content)

# Also fix Doubt Solver
old_doubt = '<ReactMarkdown components={MarkdownComponents} className="prose dark:prose-invert max-w-none prose-sm">{doubtAnswer}</ReactMarkdown>'
new_doubt = '<div className="prose dark:prose-invert max-w-none prose-sm"><ReactMarkdown components={MarkdownComponents}>{doubtAnswer}</ReactMarkdown></div>'
content = content.replace(old_doubt, new_doubt)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
