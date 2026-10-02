import re

with open("src/contexts/ThemeContext.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Remove font-weight: bold from active link
content = content.replace("font-weight: bold;", "/* font-weight: bold; removed to prevent text jitter */")

with open("src/contexts/ThemeContext.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
