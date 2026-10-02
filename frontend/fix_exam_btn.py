import re

with open("src/pages/ExamDashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_btns = """<Link to="/notes" className={`btn-base px-4 py-2 text-sm rounded-lg flex items-center gap-2 font-semibold shadow-sm border transition-colors ${task.completed ? 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50' : 'bg-white border-blue-200 text-blue-700 hover:bg-blue-50'}`}>
                                <BookOpen size={16} /> Read Notes
                              </Link>"""

new_btns = """<Link to={`/exam/${id}/prep/${encodeURIComponent(task.topic)}`} className={`btn-base px-4 py-2 text-sm rounded-lg flex items-center gap-2 font-semibold shadow-sm border transition-colors ${task.completed ? 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400' : 'bg-white border-purple-200 text-purple-700 hover:bg-purple-50 dark:bg-gray-800 dark:border-purple-900/30 dark:text-purple-400'}`}>
                                <Brain size={16} /> Prep Mode
                              </Link>
                              <Link to="/notes" className={`btn-base px-4 py-2 text-sm rounded-lg flex items-center gap-2 font-semibold shadow-sm border transition-colors ${task.completed ? 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400' : 'bg-white border-blue-200 text-blue-700 hover:bg-blue-50 dark:bg-gray-800 dark:border-blue-900/30 dark:text-blue-400'}`}>
                                <BookOpen size={16} /> Read Notes
                              </Link>"""

content = content.replace(old_btns, new_btns)

with open("src/pages/ExamDashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
