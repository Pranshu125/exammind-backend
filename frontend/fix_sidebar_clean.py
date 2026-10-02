import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the flex-1 overflow-hidden wrapper and the 50px margin hack
content = content.replace(
    """<div className="flex-1 overflow-hidden">
        <nav className="h-full pl-4 space-y-1 pt-4 overflow-y-auto pb-6 custom-scrollbar" style={{ marginRight: '-50px', paddingRight: '50px' }}>""",
    """<nav className="flex-1 pl-4 pr-0 space-y-1 pt-4 overflow-y-auto pb-6 custom-scrollbar">"""
)

# Remove the closing div for the wrapper
content = content.replace(
    """</nav>
      </div>""",
    """</nav>"""
)

# Ensure sidebar-container has the -mr-[1px] overlap but NO overflow-hidden (overflow-hidden might clip the overlap or cause issues)
content = content.replace(
    """<div className="sidebar-container w-64 h-full flex flex-col relative z-50 overflow-hidden -mr-[1px]">""",
    """<div className="sidebar-container w-64 h-full flex flex-col relative z-50 -mr-[1px]">"""
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
