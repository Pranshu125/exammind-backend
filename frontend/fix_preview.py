import re

with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_notes_ui = """<div className="relative">
          <div className="prose dark:prose-invert max-w-none bg-white dark:bg-gray-800 p-8 pb-32 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
            <ReactMarkdown>{content.notes}</ReactMarkdown>
          </div>
          
          <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-white via-white to-transparent dark:from-gray-800 dark:via-gray-800 rounded-b-2xl flex justify-center items-end h-40">
            <button 
              onClick={() => {
                setChatMode(true);
                if(messages.length === 0) {
                   setMessages([{ role: 'assistant', content: `I've prepared notes on **${decodedTopic}**. What specific part would you like to discuss or have explained further?` }]);
                }
              }}
              className="bg-[var(--matte-primary)] text-white px-8 py-3 rounded-xl font-bold shadow-lg hover:-translate-y-1 hover:shadow-xl transition-all flex items-center gap-2"
            >
              <MessageCircle size={20} /> Discuss these Notes
            </button>
          </div>
        </div>"""

new_notes_ui = """<div className="relative">
          <div className="prose dark:prose-invert max-w-none bg-white dark:bg-gray-800 p-8 pb-32 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 max-h-[600px] overflow-hidden">
            <ReactMarkdown>{content.notes}</ReactMarkdown>
          </div>
          
          <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-white via-white/80 to-transparent dark:from-gray-800 dark:via-gray-800/80 rounded-b-2xl flex justify-center items-end h-64">
            <button 
              onClick={() => {
                setChatMode(true);
                if(messages.length === 0) {
                   setMessages([{ role: 'assistant', content: `I've prepared notes on **${decodedTopic}**. What specific part would you like to discuss or have explained further?` }]);
                }
              }}
              className="bg-[var(--matte-primary)] text-white px-8 py-4 rounded-xl font-bold shadow-2xl hover:-translate-y-1 hover:shadow-3xl transition-all flex items-center gap-2 text-lg"
            >
              <MessageCircle size={24} /> Enter Full Notes & Chat Mode
            </button>
          </div>
        </div>"""

content = content.replace(old_notes_ui, new_notes_ui)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
