import re

with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace chatMode render
old_chat = """<div className="flex flex-col h-[600px] bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden relative">
          <div className="p-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 flex justify-between items-center">
            <div>
              <h3 className="font-bold text-lg flex items-center gap-2"><MessageCircle size={18} /> Discuss Notes</h3>
              <p className="text-sm text-gray-500">Ask any follow-up questions about {decodedTopic}</p>
            </div>
            <button onClick={() => setChatMode(false)} className="px-4 py-2 text-sm font-medium bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
              Return to Notes
            </button>
          </div>
          
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 mt-10">
                <Sparkles className="w-12 h-12 mx-auto mb-4 opacity-20" />
                <p>Hello! I am your AI tutor. Ask me anything about {decodedTopic}!</p>
              </div>
            )}
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] rounded-2xl p-4 ${msg.role === 'user' ? 'bg-[var(--matte-primary)] text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'}`}>
                  <ReactMarkdown className="prose dark:prose-invert max-w-none prose-sm">
                    {msg.content}
                  </ReactMarkdown>
                </div>
              </div>
            ))}
            {chatLoading && (
              <div className="flex justify-start">
                <div className="max-w-[80%] rounded-2xl p-4 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                  <Loader2 className="w-5 h-5 animate-spin" />
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <form onSubmit={handleSendMessage} className="p-4 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 flex gap-2">
            <input 
              type="text" 
              value={inputMsg}
              onChange={e => setInputMsg(e.target.value)}
              placeholder="Ask a question..." 
              className="flex-1 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-[var(--matte-primary)]"
            />
            <button type="submit" disabled={!inputMsg.trim() || chatLoading} className="bg-[var(--matte-primary)] text-white p-3 rounded-xl hover:opacity-90 disabled:opacity-50">
              <Send size={20} />
            </button>
          </form>
        </div>"""

new_chat = """<div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[700px]">
          <div className="flex flex-col bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden relative">
            <div className="p-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 flex justify-between items-center shrink-0">
              <h3 className="font-bold text-lg flex items-center gap-2"><BookOpen size={18} /> Full Study Notes</h3>
              <button onClick={() => setChatMode(false)} className="px-4 py-2 text-sm font-medium bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                Exit
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-6 prose dark:prose-invert max-w-none prose-sm">
              <ReactMarkdown>{content.notes}</ReactMarkdown>
            </div>
          </div>
          
          <div className="flex flex-col bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden relative">
            <div className="p-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 shrink-0">
              <h3 className="font-bold text-lg flex items-center gap-2"><MessageCircle size={18} /> Discuss Notes</h3>
              <p className="text-sm text-gray-500">Ask any follow-up questions about {decodedTopic}</p>
            </div>
            
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {messages.length === 0 && (
                <div className="text-center text-gray-500 mt-10">
                  <Sparkles className="w-12 h-12 mx-auto mb-4 opacity-20" />
                  <p>Hello! I am your AI tutor. Ask me anything about {decodedTopic}!</p>
                </div>
              )}
              {messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[85%] rounded-2xl p-4 ${msg.role === 'user' ? 'bg-[var(--matte-primary)] text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'}`}>
                    <ReactMarkdown className="prose dark:prose-invert max-w-none prose-sm">
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                </div>
              ))}
              {chatLoading && (
                <div className="flex justify-start">
                  <div className="max-w-[85%] rounded-2xl p-4 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                    <Loader2 className="w-5 h-5 animate-spin" />
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            <form onSubmit={handleSendMessage} className="p-4 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 flex gap-2 shrink-0">
              <input 
                type="text" 
                value={inputMsg}
                onChange={e => setInputMsg(e.target.value)}
                placeholder="Ask a question..." 
                className="flex-1 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-[var(--matte-primary)]"
              />
              <button type="submit" disabled={!inputMsg.trim() || chatLoading} className="bg-[var(--matte-primary)] text-white p-3 rounded-xl hover:opacity-90 disabled:opacity-50">
                <Send size={20} />
              </button>
            </form>
          </div>
        </div>"""

content = content.replace(old_chat, new_chat)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
