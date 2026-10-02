with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the email span
content = content.replace(
    '<span className="text-[11px] font-semibold text-gray-500 truncate">{currentUser?.email}</span>',
    ''
)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
