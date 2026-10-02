import re

with open("src/pages/ExamDashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace hardcoded blue progress bar with theme color
old_bar = """<div className="bg-blue-500 h-2 rounded-full transition-all duration-1000" style={{ width: `${progressPercent}%` }}></div>"""
new_bar = """<div className="h-2 rounded-full transition-all duration-1000" style={{ width: `${progressPercent}%`, backgroundColor: 'var(--matte-primary)' }}></div>"""

content = content.replace(old_bar, new_bar)

# Replace the background of the track if it was hardcoded (bg-white/10 might actually be okay for dark mode, but let's use matte-primary-light to be consistent)
old_track = """<div className="w-full bg-white/10 rounded-full h-2 mb-4">"""
new_track = """<div className="w-full rounded-full h-2 mb-4" style={{ backgroundColor: 'var(--matte-primary-light)' }}>"""

content = content.replace(old_track, new_track)

with open("src/pages/ExamDashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
