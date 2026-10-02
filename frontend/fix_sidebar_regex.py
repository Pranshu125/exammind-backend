import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Profile
content = re.sub(
    r"className=\{\`flex items-center gap-3 p-2 -ml-2 rounded-xl transition-colors hover:bg-gray-100\s*\n\$\{location\.pathname === '/profile' \? 'bg-gray-200/60' : ''\}\`\}",
    r"className={`sidebar-link flex items-center gap-3 p-2 -ml-2 rounded-xl transition-colors text-sm font-medium ${location.pathname === '/profile' ? 'active' : ''}`}",
    content
)

# Fix Nav Items
content = re.sub(
    r"className=\{\`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm font-medium \$\{\s*isActive\s*\?\s*'bg-gray-200/60 text-black'\s*:\s*'text-gray-600 hover:bg-gray-100 hover:text-black'\s*\}\`\}",
    r"className={`sidebar-link flex items-center gap-3 px-3 py-2 transition-colors text-sm font-medium ${isActive ? 'active' : ''}`}",
    content
)

# Fix My Exams
content = re.sub(
    r"className=\{\`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm font-medium \$\{\s*isActive\s*\?\s*'bg-blue-50 text-blue-700'\s*:\s*'text-gray-600 hover:bg-gray-100 hover:text-black'\s*\}\`\}",
    r"className={`sidebar-link flex items-center gap-3 px-3 py-2 transition-colors text-sm font-medium ${isActive ? 'active' : ''}`}",
    content
)

# Fix Settings
content = re.sub(
    r"className=\{\`flex w-full items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm font-medium \$\{\s*location\.pathname === '/settings'\s*\?\s*'bg-gray-200/60 text-black'\s*:\s*'text-gray-600 hover:bg-gray-100 hover:text-black'\s*\}\`\}",
    r"className={`sidebar-link flex w-full items-center gap-3 px-3 py-2 transition-colors text-sm font-medium ${location.pathname === '/settings' ? 'active' : ''}`}",
    content
)

# Fix Icons
content = re.sub(
    r"className=\{\`\$\{isActive \? 'text-black' : 'text-gray-400'\} transition-colors\`\}",
    r'className="sidebar-icon transition-colors"',
    content
)
content = re.sub(
    r"className=\{\`\$\{isActive \? 'text-blue-500' : 'text-gray-400'\} transition-colors\`\}",
    r'className="sidebar-icon transition-colors"',
    content
)
content = re.sub(
    r"className=\{location\.pathname === '/settings' \? 'text-black' : 'text-gray-400'\}",
    r'className="sidebar-icon transition-colors"',
    content
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
