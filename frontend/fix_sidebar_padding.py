import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Header Padding
content = content.replace(
    """<div className="pl-4 pr-0 py-6 pb-4">""",
    """<div className="pl-4 pr-0 pt-6 pb-0">"""
)

# Fix Nav Padding to accommodate the 40px fluid curves without clipping
content = content.replace(
    """<nav className="flex-1 pl-4 pr-0 space-y-1 pt-4 overflow-y-auto pb-6 custom-scrollbar">""",
    """<nav className="flex-1 pl-4 pr-0 space-y-1 pt-12 overflow-y-auto pb-12 custom-scrollbar">"""
)

# Fix Footer Padding
content = content.replace(
    """<div className="sidebar-footer pl-4 pr-0 py-4 mt-auto">""",
    """<div className="sidebar-footer pl-4 pr-0 pt-0 pb-4 mt-auto">"""
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
