with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_p = '<p className="opacity-80">{data.explanation}</p>'
new_p = '<div className="opacity-80"><ReactMarkdown components={MarkdownComponents}>{data.explanation}</ReactMarkdown></div>'

content = content.replace(old_p, new_p)

# We need to pass MarkdownComponents to QuizQuestion
content = content.replace("<QuizQuestion key={i} data={q} index={i} />", "<QuizQuestion key={i} data={q} index={i} MarkdownComponents={MarkdownComponents} />")
content = content.replace("function QuizQuestion({ data, index }) {", "function QuizQuestion({ data, index, MarkdownComponents }) {")

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
