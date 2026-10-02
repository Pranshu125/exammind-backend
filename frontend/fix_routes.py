import re

with open("src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add import for PrepMode
content = content.replace(
    "import ExamDashboard from './pages/ExamDashboard';",
    "import ExamDashboard from './pages/ExamDashboard';\nimport PrepMode from './pages/PrepMode';"
)

# Add Route inside the Dashboard layout routes. 
# Wait, Dashboard handles child routes? Let's check how ExamDashboard is routed.
