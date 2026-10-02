with open("src/components/UploadComponent.jsx", "r", encoding="utf-8") as f:
    content = f.read()

old_url_timetable = "const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';"
new_url = """const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const API_BASE = isLocalhost ? 'http://localhost:8000' : (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000');"""

content = content.replace(old_url_timetable, new_url)

with open("src/components/UploadComponent.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
