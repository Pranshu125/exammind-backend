import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the nav element with a wrapped version that pushes the scrollbar out
old_nav_start = """<nav className="flex-1 pl-4 pr-0 space-y-1 pt-4 overflow-y-auto pb-6 custom-scrollbar">"""
new_nav_start = """<div className="flex-1 overflow-hidden">
        <nav className="h-full pl-4 space-y-1 pt-4 overflow-y-auto pb-6 custom-scrollbar" style={{ marginRight: '-50px', paddingRight: '50px' }}>"""

content = content.replace(old_nav_start, new_nav_start)

# We also need to close the wrapper div where the nav ends
old_nav_end = """</nav>"""
new_nav_end = """</nav>
      </div>"""

# Only replace the first </nav> since there's only one.
content = content.replace(old_nav_end, new_nav_end, 1)


# Also ensure sidebar-container is overflow-hidden
content = content.replace(
    """<div className="sidebar-container w-64 h-full flex flex-col relative z-50 -mr-[1px]">""",
    """<div className="sidebar-container w-64 h-full flex flex-col relative z-50 overflow-hidden -mr-[1px]">"""
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
