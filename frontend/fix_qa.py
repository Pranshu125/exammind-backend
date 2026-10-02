with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace <p> for feedback
content = content.replace(
    '<p className="mt-1 text-green-800 dark:text-green-300 font-medium">{testFeedback}</p>',
    '<div className="mt-1 text-green-800 dark:text-green-300 font-medium"><ReactMarkdown components={MarkdownComponents}>{testFeedback}</ReactMarkdown></div>'
)

# Replace <p> for QA correct answer
content = content.replace(
    '<p className="mt-1 text-blue-800 dark:text-blue-300">{q.answer}</p>',
    '<div className="mt-1 text-blue-800 dark:text-blue-300"><ReactMarkdown components={MarkdownComponents}>{q.answer}</ReactMarkdown></div>'
)

# Replace <p> for general flashcard list answer
content = content.replace(
    '<p className="text-gray-700 dark:text-gray-300">{qa.answer}</p>',
    '<div className="text-gray-700 dark:text-gray-300"><ReactMarkdown components={MarkdownComponents}>{qa.answer}</ReactMarkdown></div>'
)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
