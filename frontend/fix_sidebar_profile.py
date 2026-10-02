with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Profile link
content = content.replace(
    """className={`flex items-center gap-3 p-2 -ml-2 rounded-xl transition-colors hover:bg-gray-100 
${location.pathname === '/profile' ? 'bg-gray-200/60' : ''}`}""",
    """className={`sidebar-link flex items-center gap-3 p-2 -ml-2 rounded-xl transition-colors text-sm font-medium ${
                  location.pathname === '/profile' ? 'active' : ''
                }`}"""
)
content = content.replace(
    """<p className="text-sm font-bold text-gray-900 truncate">""",
    """<p className="sidebar-title text-sm font-bold truncate">"""
)

# Fix folder link (My Exams)
content = content.replace(
    """className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm font-medium ${
                        isActive 
                          ? 'bg-blue-50 text-blue-700' 
                          : 'text-gray-600 hover:bg-gray-100 hover:text-black'
                      }`}""",
    """className={`sidebar-link flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm font-medium ${
                        isActive ? 'active' : ''
                      }`}"""
)
content = content.replace(
    """<Folder size={18} className={`${isActive ? 'text-blue-500' : 'text-gray-400'} transition-colors`} />""",
    """<Folder size={18} className="sidebar-icon transition-colors" />"""
)

content = content.replace(
    """<div className="px-3 text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">My Exams</div>""",
    """<div className="sidebar-title px-3 text-[10px] font-bold uppercase tracking-wider mb-2 opacity-70">My Exams</div>"""
)

# Fix Provider label
content = content.replace(
    """<label className="flex items-center gap-2 text-[10px] font-semibold text-gray-500 uppercase tracking-wider mb-2">""",
    """<label className="sidebar-title flex items-center gap-2 text-[10px] font-semibold uppercase tracking-wider mb-2 opacity-70">"""
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
