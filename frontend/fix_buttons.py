import re

with open("src/pages/ExamDashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# I will replace the entire div containing the buttons with just the Prep Mode button.
# Let's find the div: <div className="flex flex-wrap items-center gap-2 sm:gap-3 sm:ml-4 pl-14 sm:pl-0">

start_div = '<div className="flex flex-wrap items-center gap-2 sm:gap-3 sm:ml-4 pl-14 sm:pl-0">'
end_div = '</div>\n                            \n                          </div>\n                        </div>\n                      </div>'

# Actually, I'll use regex to replace from start_div to the closing div of that flex container.
# It's safer to just replace the inner buttons.

pattern = re.compile(r'<div className="flex flex-wrap items-center gap-2 sm:gap-3 sm:ml-4 pl-14 sm:pl-0">.*?</div>', re.DOTALL)

new_btns = """<div className="flex flex-wrap items-center gap-2 sm:gap-3 sm:ml-4 pl-14 sm:pl-0">
                              <Link to={`/exam/${id}/prep/${encodeURIComponent(task.topic)}`} className={`btn-base px-6 py-2.5 text-sm rounded-xl flex items-center gap-2 font-bold shadow-md transition-all ${task.completed ? 'bg-gray-100 text-gray-500 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-400' : 'bg-[var(--matte-primary)] text-white hover:opacity-90 hover:scale-105'}`}>
                                <Brain size={18} /> Enter Prep Mode
                              </Link>
                              
                              <button 
                                onClick={() => toggleTaskCompletion(dayIndex, taskIndex, task.completed)}
                                className={`p-2.5 rounded-xl flex items-center justify-center transition-colors ${task.completed ? 'bg-green-100 text-green-600 hover:bg-green-200 dark:bg-green-900/30 dark:text-green-500' : 'bg-gray-100 text-gray-400 hover:bg-gray-200 hover:text-gray-600 dark:bg-gray-800 dark:hover:bg-gray-700'}`}
                                title={task.completed ? "Mark as incomplete" : "Mark as complete"}
                              >
                                <CheckCircle2 size={20} />
                              </button>
                            </div>"""

content = pattern.sub(new_btns, content)

with open("src/pages/ExamDashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
