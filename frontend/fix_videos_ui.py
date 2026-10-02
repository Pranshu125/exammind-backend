with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

import re

old_video_render = """        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {content.videos.map((vid, i) => ("""

new_video_render = """        if (Array.isArray(content.videos) && content.videos.length === 0) {
          return (
            <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 text-center max-w-lg mx-auto mt-10">
              <Video className="w-12 h-12 mx-auto text-gray-400 mb-4" />
              <h2 className="text-2xl font-bold mb-2">No Videos Found</h2>
              <p className="text-gray-600 dark:text-gray-400 mb-6">We couldn't find any video tutorials for this topic. It might be a temporary search limit.</p>
              <button onClick={() => { setContent(prev => ({...prev, videos: null})); fetchNotesOrVideos('videos'); }} className="bg-[var(--matte-primary)] text-white font-bold py-2 px-6 rounded-xl hover:opacity-90 transition-all">Try Again</button>
            </div>
          );
        }
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {content.videos.map((vid, i) => ("""

content = content.replace(old_video_render, new_video_render)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
