import re

with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add scrollbarGutter to main
content = content.replace(
    """<main className="flex-1 overflow-x-hidden overflow-y-auto bg-transparent">""",
    """<main className="flex-1 overflow-x-hidden overflow-y-auto bg-transparent" style={{ scrollbarGutter: 'stable' }}>"""
)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    sidebar_content = f.read()

# Add shrink-0 to sidebar container to prevent flex resizing
sidebar_content = sidebar_content.replace(
    """<div className="sidebar-container w-64 h-full flex flex-col relative z-50 -mr-[1px]">""",
    """<div className="sidebar-container w-64 h-full flex flex-col relative z-50 -mr-[1px] shrink-0">"""
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(sidebar_content)

print("done")
