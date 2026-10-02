with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix QA crash
old_qa_render = """    if (activeTab === 'qa' && content.qa) {
      if (testMode) {"""
new_qa_render = """    if (activeTab === 'qa' && content.qa) {
      if (typeof content.qa === 'string') {
        return (
          <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-red-100 dark:border-red-900/30 text-center max-w-lg mx-auto mt-10">
            <h2 className="text-2xl font-bold mb-2 text-red-600 dark:text-red-400">Error Loading Q&A</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">{content.qa}</p>
            <button onClick={() => { setContent(prev => ({...prev, qa: null})); }} className="bg-[var(--matte-primary)] text-white font-bold py-2 px-6 rounded-xl hover:opacity-90 transition-all">Retry</button>
          </div>
        );
      }
      if (testMode) {"""
content = content.replace(old_qa_render, new_qa_render)

# Fix Quiz crash
old_quiz_render = """    if (activeTab === 'quiz' && content.quiz) {
      return ("""
new_quiz_render = """    if (activeTab === 'quiz' && content.quiz) {
      if (typeof content.quiz === 'string') {
        return (
          <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-red-100 dark:border-red-900/30 text-center max-w-lg mx-auto mt-10">
            <h2 className="text-2xl font-bold mb-2 text-red-600 dark:text-red-400">Error Loading Quiz</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">{content.quiz}</p>
            <button onClick={() => { setContent(prev => ({...prev, quiz: null})); }} className="bg-[var(--matte-primary)] text-white font-bold py-2 px-6 rounded-xl hover:opacity-90 transition-all">Retry</button>
          </div>
        );
      }
      return ("""
content = content.replace(old_quiz_render, new_quiz_render)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
