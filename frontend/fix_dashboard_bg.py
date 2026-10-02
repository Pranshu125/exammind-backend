with open("src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Make the outer container transparent so it uses the body's matte-bg
content = content.replace(
    """<div className="flex h-screen bg-gray-50 font-sans w-full overflow-hidden text-gray-900">""",
    """<div className="flex h-screen bg-transparent font-sans w-full overflow-hidden text-gray-900">"""
)

# Also check for main area background just in case
content = content.replace(
    """<main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50">""",
    """<main className="flex-1 overflow-x-hidden overflow-y-auto bg-transparent">"""
)

with open("src/pages/Dashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
