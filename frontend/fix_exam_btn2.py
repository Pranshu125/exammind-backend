import re

with open("src/pages/ExamDashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find the exact block using regex to be safe
pattern = re.compile(r'<Link to="/notes" className=\{`btn-base[^>]*>\s*<BookOpen size=\{16\} /> Read Notes\s*</Link>')

new_btns = """<Link to={`/exam/${id}/prep/${encodeURIComponent(task.topic)}`} className={`btn-base px-4 py-2 text-sm rounded-lg flex items-center gap-2 font-semibold shadow-sm border transition-colors ${task.completed ? 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50' : 'bg-white border-purple-200 text-purple-700 hover:bg-purple-50'}`}>
                                <Brain size={16} /> Prep Mode
                              </Link>
                              <Link to="/notes" className={`btn-base px-4 py-2 text-sm rounded-lg flex items-center gap-2 font-semibold shadow-sm border transition-colors ${task.completed ? 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50' : 'bg-white border-blue-200 text-blue-700 hover:bg-blue-50'}`}>
                                <BookOpen size={16} /> Read Notes
                              </Link>"""

content = pattern.sub(new_btns, content)

with open("src/pages/ExamDashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
