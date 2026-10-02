import re

with open("src/components/CustomSelect.jsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    """<div className="flex items-center gap-2 overflow-hidden text-sm md:text-base">""",
    """<div className={`flex items-center gap-2 overflow-hidden ${size === 'small' ? '' : 'text-sm md:text-base'}`}>"""
)

with open("src/components/CustomSelect.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
