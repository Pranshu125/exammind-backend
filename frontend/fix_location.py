with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the incorrectly placed line
content = content.replace("  const location = useLocation();\n", "")

# Add it at the top of the component
old_start = "export default function Dashboard() {\n  const [mobileSidebarOpen"
new_start = "export default function Dashboard() {\n  const location = useLocation();\n  const [mobileSidebarOpen"

content = content.replace(old_start, new_start)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
