with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Make the outer div use sidebar-container
content = content.replace(
    """<div className="w-64 bg-gray-50 h-full flex flex-col relative z-50 border-r border-gray-200">""",
    """<div className="sidebar-container w-64 h-full flex flex-col relative z-50 border-r border-gray-200">"""
)

# Fix inner active/hover states to use sidebar specific classes
content = content.replace(
    """className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm font-medium ${
                  isActive 
                    ? 'bg-gray-200/60 text-black' 
                    : 'text-gray-600 hover:bg-gray-100 hover:text-black'
                }`}""",
    """className={`sidebar-link flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm font-medium ${
                  isActive ? 'active' : ''
                }`}"""
)

content = content.replace(
    """<Icon size={18} className={`${isActive ? 'text-black' : 'text-gray-400'} transition-colors`} />""",
    """<Icon size={18} className="sidebar-icon transition-colors" />"""
)

# Remove bg-gray-50 from footer part
content = content.replace(
    """<div className="p-4 bg-gray-50 mt-auto border-t border-gray-200">""",
    """<div className="sidebar-footer p-4 mt-auto border-t border-gray-200">"""
)

# Settings link
content = content.replace(
    """className={`flex w-full items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm font-medium ${
              location.pathname === '/settings' 
                ? 'bg-gray-200/60 text-black' 
                : 'text-gray-600 hover:bg-gray-100 hover:text-black'
            }`}""",
    """className={`sidebar-link flex w-full items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm font-medium ${
              location.pathname === '/settings' ? 'active' : ''
            }`}"""
)
content = content.replace(
    """<Settings size={18} className={location.pathname === '/settings' ? 'text-black' : 'text-gray-400'} />""",
    """<Settings size={18} className="sidebar-icon transition-colors" />"""
)

# Header Title
content = content.replace(
    """<h1 className="text-xl font-bold tracking-tight text-black mb-8 flex items-center gap-2">""",
    """<h1 className="sidebar-title text-xl font-bold tracking-tight mb-8 flex items-center gap-2">"""
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
