import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Provider Margin
content = content.replace(
    """<div className="pr-4 mb-2">
            <label className="sidebar-title flex items-center gap-2 text-[10px] font-semibold uppercase tracking-wider mb-2 opacity-70">
              <Cpu size={12} /> Provider""",
    """<div className="pr-4 mb-10">
            <label className="sidebar-title flex items-center gap-2 text-[10px] font-semibold uppercase tracking-wider mb-2 opacity-70">
              <Cpu size={12} /> Provider"""
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
