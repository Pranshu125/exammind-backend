with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the nav container to prevent clipping and fix scrollbars
content = content.replace(
    """<nav className="flex-1 pl-4 pr-0 space-y-1 mt-4 overflow-y-auto pb-6 overflow-x-hidden">""",
    """<nav className="flex-1 pl-4 pr-0 space-y-1 pt-4 overflow-y-auto pb-6 custom-scrollbar">"""
)

# Also ensure Profile link in header is not clipped.
# The header has py-6, which should give enough room for the top curve of Profile link.

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("done")
