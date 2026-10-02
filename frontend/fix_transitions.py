with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Make sidebar and padding transitions ultra-smooth
# Replace `duration-300 ease-in-out` with `duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)]`
content = content.replace("duration-300 ease-in-out", "duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)]")

# Make the page switching transition better
old_page_trans = 'animate-in fade-in slide-in-from-bottom-4 duration-500'
new_page_trans = 'animate-in fade-in zoom-in-[0.98] slide-in-from-bottom-2 duration-500 ease-[cubic-bezier(0.2,0.8,0.2,1)]'
content = content.replace(old_page_trans, new_page_trans)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
