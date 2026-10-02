with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "if (chatMode) {" in line:
        start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx + 1, len(lines)):
        if "if (loading) {" in lines[i]:
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    new_block = """      if (chatMode) {
        return (
          <div className="flex flex-col bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 h-[800px] relative overflow-hidden">
            <div className="p-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 flex justify-between items-center shrink-0">
              <h3 className="font-bold text-lg flex items-center gap-2"><BookOpen size={18} /> Full Study Notes & Discussion</h3>
              <button onClick={() => setChatMode(false)} className="px-4 py-2 text-sm font-medium bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                Exit
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-8 space-y-8 pb-32">
              <div className="prose dark:prose-invert max-w-none prose-sm">
                <ReactMarkdown components={MarkdownComponents}>{content.notes}</ReactMarkdown>
              </div>

              <div className="flex items-center gap-4 my-8">
                <div className="h-px bg-gray-200 dark:bg-gray-700 flex-1"></div>
                <span className="text-gray-400 dark:text-gray-500 text-sm font-medium">Ask questions about these notes</span>
                <div className="h-px bg-gray-200 dark:bg-gray-700 flex-1"></div>
              </div>

              <div className="space-y-6">
                {messages.length === 0 && (
                  <div className="text-center text-gray-500 mt-10">
                    <p>No questions yet. Ask anything below!</p>
                  </div>
                )}
                {messages.map((msg, i) => (
                  <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] rounded-2xl p-4 ${msg.role === 'user' ? 'bg-[var(--matte-primary)] text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'}`}>
                      <div className="prose dark:prose-invert max-w-none prose-sm"><ReactMarkdown components={MarkdownComponents}>{msg.content}</ReactMarkdown></div>
                    </div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="max-w-[85%] rounded-2xl p-4 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100"><Loader2 className="w-5 h-5 animate-spin" /></div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>
            </div>

            <div className="p-4 bg-gray-50 dark:bg-gray-900/80 border-t border-gray-100 dark:border-gray-700 shrink-0 backdrop-blur-sm absolute bottom-0 left-0 right-0 z-10">
              <form onSubmit={handleSendMessage} className="flex gap-2">
                <input type="text" value={inputMsg} onChange={e => setInputMsg(e.target.value)} placeholder="Ask a question..." className="flex-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-xl px-4 py-3 outline-none focus:border-[var(--matte-primary)]" />
                <button type="submit" disabled={chatLoading || !inputMsg.trim()} className="bg-[var(--matte-primary)] text-white px-6 rounded-xl font-bold hover:opacity-90 disabled:opacity-50 transition-opacity flex items-center justify-center">
                  <Send size={18} />
                </button>
              </form>
            </div>
          </div>
        );
      }\n\n"""
    
    final_lines = lines[:start_idx] + [new_block] + lines[end_idx:]
    with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
        f.writelines(final_lines)
    print("Replaced layout successfully")
else:
    print(f"Failed to find indices. Start: {start_idx}, End: {end_idx}")

