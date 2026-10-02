import re

with open("src/components/HomeDashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace COLORS array
old_colors = "const COLORS = ['#22c55e', '#e5e7eb'];"
new_colors = "const COLORS = ['var(--matte-primary)', 'var(--matte-primary-light)'];"

content = content.replace(old_colors, new_colors)

# Replace the legend dots to use the CSS variables via style tag instead of Tailwind classes
# Old: <div className="w-3 h-3 rounded-full bg-green-500"></div>
# New: <div className="w-3 h-3 rounded-full" style={{ backgroundColor: 'var(--matte-primary)' }}></div>

old_legend_completed = """<div className="w-3 h-3 rounded-full bg-green-500"></div>"""
new_legend_completed = """<div className="w-3 h-3 rounded-full" style={{ backgroundColor: 'var(--matte-primary)' }}></div>"""

old_legend_remaining = """<div className="w-3 h-3 rounded-full bg-gray-200"></div>"""
new_legend_remaining = """<div className="w-3 h-3 rounded-full" style={{ backgroundColor: 'var(--matte-primary-light)' }}></div>"""

content = content.replace(old_legend_completed, new_legend_completed)
content = content.replace(old_legend_remaining, new_legend_remaining)

with open("src/components/HomeDashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
