import re

with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Add import
content = content.replace(
    "import ExamDashboard from '../pages/ExamDashboard';",
    "import ExamDashboard from '../pages/ExamDashboard';\nimport PrepMode from '../pages/PrepMode';"
)

# Add Route
content = content.replace(
    """<Route path="/exam/:id" element={<ExamDashboard />} />""",
    """<Route path="/exam/:id" element={<ExamDashboard />} />\n              <Route path="/exam/:id/prep/:topic" element={<PrepMode />} />"""
)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
