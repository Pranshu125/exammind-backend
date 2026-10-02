import re

with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "import ExamDashboard from './ExamDashboard';",
    "import ExamDashboard from './ExamDashboard';\nimport PrepMode from './PrepMode';"
)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
