import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Use regex to find the exact div wrapping the provider
content = re.sub(r'<div className="pr-4 mb-2">\s*<label className="sidebar-title', r'<div className="pr-4 mb-10">\n            <label className="sidebar-title', content)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
