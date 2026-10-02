import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Find the logo img container
old_logo = """<div className="w-8 h-8 rounded-full overflow-hidden shrink-0 border border-gray-700 shadow-sm flex items-center justify-center">
              <img src="/logo.jpg" alt="Logo" className="w-full h-full object-cover" />
            </div>"""

new_logo = """<div className="w-8 h-8 rounded-xl flex items-center justify-center shrink-0 shadow-sm" style={{ backgroundColor: 'var(--matte-primary-light)' }}>
              <Sparkles size={18} className="text-white" />
            </div>"""

content = content.replace(old_logo, new_logo)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
