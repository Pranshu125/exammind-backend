with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix the loading state to actually render a loader when fetching notes/videos
old_render_content = "    const renderContent = () => {"
new_render_content = """    const renderContent = () => {
      if (loading) {
        return (
          <div className="flex flex-col items-center justify-center py-20 text-gray-500">
            <Loader2 className="w-12 h-12 animate-spin mb-4 text-[var(--matte-primary)]" />
            <p className="font-medium">Curating your {activeTab}...</p>
          </div>
        );
      }
"""
if "Curating your {activeTab}" not in content:
    content = content.replace(old_render_content, new_render_content)

# 2. Fix the regex for Mermaid
content = content.replace("replace(/\\\\n$/, '')", "replace(/\\n$/, '')")

# 3. Check what happens if content.notes is a string and it starts chatMode
# In chatMode, we render content.notes. If it's an error string, it renders fine. But if it's null, we shouldn't enter chatMode!
# We don't really need to do anything there, ReactMarkdown gracefully handles strings.

# Wait, the complete blank screen (Image 2) might be because chatMode rendering returns a Grid but we are STILL missing the Back button and Prep Mode header!
# Look at the return of PrepMode component:
"""
    return (
      <div className="min-h-screen bg-transparent w-full overflow-y-auto" style={{ scrollbarGutter: 'stable' }}>
        <div className="max-w-5xl mx-auto px-6 py-12">
          <button onClick={() => navigate(`/exam/${id}`)} className="flex items-center gap-2 text-sm font-medium text-gray-500 hover:text-gray-900 dark:hover:text-gray-100 mb-8 transition-colors">
            <ArrowLeft size={16} /> Back to Curriculum
          </button>
  
          <div className="flex items-center gap-4 mb-10">
...
"""
# If there's a fatal crash, none of this renders. What is crashing?
# Ah! "if (typeof parsed === 'string') { parsed = JSON.parse(...) }"
# If the notes or QA generated is an error string, e.g. "Failed to load: ...", and it goes to QA:
# Wait! fetchNotesOrVideos parses `data.notes` and `setContent`. 
# It sets `content[tabId] = data.videos` or `markdownText`. It does NOT call JSON.parse!
# `generateQAOrQuiz` calls JSON.parse!
# `parsed = JSON.parse(parsed.replace(...))`
# If the AI failed and returned text, JSON.parse THROWS A SYNTAX ERROR!
# If it throws a syntax error, it's inside `try { ... } catch (error) { setContent("Failed to load...") }`. So it is caught!

# What if `messages.map` throws? 
# "messages" is initialized to `[]`. So it's safe.

# Let's inspect the exact lines where the React unhandled exception happened:
# "TypeError: content.videos.map is not a function" was in my old code, which I FIXED in task-3203.
# In Image 2, the screen is blank. WHY IS IT BLANK?
# Because `chatMode` is true, it tries to render `ReactMarkdown` with `content.notes`.
# If `content.notes` is `Failed to load: Failed to fetch`.
# Wait, look at the error log from task-3193 when I started Vite:
# There are no crash errors for `ReactMarkdown` in the logs! The logs only showed the old `TypeError: content.videos.map is not a function` from before I fixed it.
# Wait, is the user's browser STILL holding an old cached version or did the Vite Hot Reload fail because of the syntax error I temporarily had?
# No, Vite successfully hot reloaded.

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
