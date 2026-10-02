import re

with open("src/components/Sidebar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the active background and fix hover for dark theme
old_link = """<Link 
            to="/profile"
            onClick={onClose}
            className={`flex items-center gap-3 p-2 -ml-2 rounded-xl  hover:bg-gray-100 ${location.pathname === '/profile' ? 'bg-gray-200/60' : ''}`}
          >"""

new_link = """<Link 
            to="/profile"
            onClick={onClose}
            className="flex items-center gap-3 p-2 -ml-2 rounded-xl transition-all hover:bg-white/10"
          >"""

content = content.replace(old_link, new_link)

with open("src/components/Sidebar.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
