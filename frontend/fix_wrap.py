import re

with open("src/pages/ExamDashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    """<div className="flex items-center gap-3 sm:ml-4 pl-14 sm:pl-0">""",
    """<div className="flex flex-wrap items-center gap-2 sm:gap-3 sm:ml-4 pl-14 sm:pl-0">"""
)

with open("src/pages/ExamDashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
