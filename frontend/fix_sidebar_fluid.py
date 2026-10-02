with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove right border from sidebar-container
content = content.replace(
    "sidebar-container w-64 h-full flex flex-col relative z-50 border-r border-gray-200",
    "sidebar-container w-64 h-full flex flex-col relative z-50"
)

# 2. Fix Header padding
content = content.replace(
    """<div className="p-6 pb-4">""",
    """<div className="pl-4 pr-0 py-6 pb-4">"""
)
# Ensure Header title has padding so it doesn't touch edge
content = content.replace(
    """<h1 className="sidebar-title text-xl font-bold tracking-tight mb-8 flex items-center gap-2">""",
    """<h1 className="sidebar-title text-xl font-bold tracking-tight mb-8 flex items-center gap-2 pr-4">"""
)

# 3. Fix Nav padding
content = content.replace(
    """<nav className="flex-1 px-3 space-y-1 mt-4 overflow-y-auto pb-6">""",
    """<nav className="flex-1 pl-4 pr-0 space-y-1 mt-4 overflow-y-auto pb-6 overflow-x-hidden">"""
)
# Fix "My Exams" title
content = content.replace(
    """<div className="sidebar-title px-3 text-[10px]""",
    """<div className="sidebar-title px-0 text-[10px]"""
)

# 4. Fix Footer padding
content = content.replace(
    """<div className="sidebar-footer p-4 mt-auto border-t border-gray-200">""",
    """<div className="sidebar-footer pl-4 pr-0 py-4 mt-auto">"""
)
# Fix Provider select wrapper
content = content.replace(
    """<div className="px-1 mb-2">""",
    """<div className="pr-4 mb-2">"""
)

# 5. Make sure all sidebar-links have basic uniform padding internally
# Previously they had px-3 or p-2. Let's let CSS handle some of it or just leave it.

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
