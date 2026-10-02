with open("src/pages/PrepMode.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_video_render = """    if (activeTab === 'videos' && content.videos) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {content.videos.map((vid, i) => (
            <a key={i} href={vid.url} target="_blank" rel="noopener noreferrer" className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden hover:border-red-300 hover:shadow-md transition-all group flex flex-col">
              <div className="w-full h-40 bg-gray-200 dark:bg-gray-900 relative overflow-hidden">
                {vid.thumbnail ? (
                   <img src={vid.thumbnail} alt={vid.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                ) : (
                   <div className="absolute inset-0 flex items-center justify-center text-red-500"><Video size={48} className="opacity-20" /></div>
                )}
                <div className="absolute inset-0 bg-black/20 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                   <PlayCircle size={48} className="text-white drop-shadow-lg" />
                </div>
              </div>
              <div className="p-5 flex-1 flex flex-col justify-between">
                <div>
                  <h3 className="font-bold text-sm mb-2 line-clamp-2">{vid.title}</h3>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{vid.channel_title || "YouTube"}</p>
                </div>
                <div className="mt-4 flex items-center gap-1 text-xs font-semibold text-red-600">
                  Watch Video <ExternalLink size={12} />
                </div>
              </div>
            </a>
          ))}
        </div>
      );
    }"""

new_video_render = """    if (activeTab === 'videos' && content.videos) {
      if (typeof content.videos === 'string') {
        return (
          <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-sm border border-red-100 dark:border-red-900/30 text-center max-w-lg mx-auto mt-10">
            <Video className="w-12 h-12 mx-auto text-red-400 mb-4" />
            <h2 className="text-2xl font-bold mb-2 text-red-600 dark:text-red-400">Error Loading Videos</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">{content.videos}</p>
            <button onClick={() => { setContent(prev => ({...prev, videos: null})); fetchNotesOrVideos('videos'); }} className="bg-[var(--matte-primary)] text-white font-bold py-2 px-6 rounded-xl hover:opacity-90 transition-all">Retry</button>
          </div>
        );
      }
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {content.videos.map((vid, i) => (
            <a key={i} href={vid.video_id?.startsWith('http') ? vid.video_id : `https://www.youtube.com/watch?v=${vid.video_id}`} target="_blank" rel="noopener noreferrer" className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden hover:border-red-300 hover:shadow-md transition-all group flex flex-col">
              <div className="w-full h-40 bg-gray-200 dark:bg-gray-900 relative overflow-hidden">
                {vid.thumbnail_url ? (
                   <img src={vid.thumbnail_url} alt={vid.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                ) : (
                   <div className="absolute inset-0 flex items-center justify-center text-red-500"><Video size={48} className="opacity-20" /></div>
                )}
                <div className="absolute inset-0 bg-black/20 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                   <PlayCircle size={48} className="text-white drop-shadow-lg" />
                </div>
              </div>
              <div className="p-5 flex-1 flex flex-col justify-between">
                <div>
                  <h3 className="font-bold text-sm mb-2 line-clamp-2">{vid.title}</h3>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{vid.channel_title || "YouTube"}</p>
                </div>
                <div className="mt-4 flex items-center gap-1 text-xs font-semibold text-red-600">
                  Watch Video <ExternalLink size={12} />
                </div>
              </div>
            </a>
          ))}
        </div>
      );
    }"""

content = content.replace(old_video_render, new_video_render)

with open("src/pages/PrepMode.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
