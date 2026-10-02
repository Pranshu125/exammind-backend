import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add a tiny 1px negative right margin to the entire sidebar container to overlap the dashboard and destroy seams
content = content.replace(
    """<div className="sidebar-container w-64 h-full flex flex-col relative z-50">""",
    """<div className="sidebar-container w-64 h-full flex flex-col relative z-50 -mr-[1px]">"""
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
