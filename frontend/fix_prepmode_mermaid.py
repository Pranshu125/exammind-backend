import re

with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add imports
if "import MermaidRenderer" not in content:
    content = content.replace("import ReactMarkdown from 'react-markdown';", "import ReactMarkdown from 'react-markdown';\nimport MermaidRenderer from '../components/MermaidRenderer';")

# Add components definition inside PrepMode
comp_def = """
  const MarkdownComponents = {
    code({node, inline, className, children, ...props}) {
      const match = /language-(\w+)/.exec(className || '')
      if (!inline && match && match[1] === 'mermaid') {
        return <MermaidRenderer chart={String(children).replace(/\n$/, '')} />
      }
      return <code className={className} {...props}>{children}</code>
    }
  };
"""
if "const MarkdownComponents =" not in content:
    content = content.replace("const API_BASE = ", comp_def + "\n  const API_BASE = ")

# Replace <ReactMarkdown> with <ReactMarkdown components={MarkdownComponents}>
content = content.replace("<ReactMarkdown>", "<ReactMarkdown components={MarkdownComponents}>")
content = content.replace('<ReactMarkdown className="prose dark:prose-invert max-w-none prose-sm">', '<ReactMarkdown components={MarkdownComponents} className="prose dark:prose-invert max-w-none prose-sm">')

# Also update the chat prompt to tell it to use Mermaid
old_qa_prompt = 'content: `Generate exactly ${settings.numQuestions} important Question and Answer pairs for studying the topic: "${decodedTopic}" at a ${settings.difficulty} difficulty level. Return ONLY a JSON array of objects with "question" and "answer" keys. No markdown blocks, just raw JSON.`'
new_qa_prompt = 'content: `Generate exactly ${settings.numQuestions} important Question and Answer pairs for studying the topic: "${decodedTopic}" at a ${settings.difficulty} difficulty level. If a diagram helps, include a Mermaid.js markdown block in the answer string. Return ONLY a JSON array of objects with "question" and "answer" keys. Return raw JSON without wrapping in markdown blocks.`'
content = content.replace(old_qa_prompt, new_qa_prompt)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
