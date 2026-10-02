import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the specific className string with the new one using regex
pattern = r'className=\{`flex items-center gap-3 p-2 -ml-2 rounded-xl\s+hover:bg-gray-100 \$\{location\.pathname === \'/profile\' \? \'bg-gray-200/60\' : \'\'\}`\}'
replacement = r'className="flex items-center gap-3 p-2 -ml-2 rounded-xl transition-all hover:bg-white/10"'

content = re.sub(pattern, replacement, content)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
