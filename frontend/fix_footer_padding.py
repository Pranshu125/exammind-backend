import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Footer Padding to accommodate the bottom curve
content = content.replace(
    """<div className="sidebar-footer pl-4 pr-0 pt-0 pb-4 mt-auto">""",
    """<div className="sidebar-footer pl-4 pr-0 pt-4 pb-12 mt-auto">"""
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
