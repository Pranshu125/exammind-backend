import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Change mb-10 to mb-6
content = content.replace(
    """<div className="pr-4 mb-10">""",
    """<div className="pr-4 mb-6">"""
)

# Pass size="small" to CustomSelect
content = content.replace(
    """<CustomSelect 
              value={engine}""",
    """<CustomSelect 
              size="small"
              value={engine}"""
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
